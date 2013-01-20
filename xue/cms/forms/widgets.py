# -*- coding: utf-8 -*-

from os.path import join as pathjoin
import copy

from itertools import chain

from django.conf import settings
from django.contrib.sites.models import Site
from django.forms.widgets import Select, MultiWidget, Widget
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.forms.util import flatatt
from django.utils.datastructures import MultiValueDict, MergeDict
from django.utils.encoding import force_unicode
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from cms.forms.utils import get_site_choices, get_page_choices
from cms.models import Page, PageUser, Placeholder
from cms.plugin_pool import plugin_pool
from cms.utils import get_language_from_request


class PageSelectWidget(MultiWidget):
    """A widget that allows selecting a page by first selecting a site and then
    a page on that site in a two step process.
    """
    def __init__(self, site_choices=None, page_choices=None, attrs=None):
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            self.attrs = {}
        if site_choices is None or page_choices is None:
            site_choices, page_choices = get_site_choices(), get_page_choices()
        self.site_choices = site_choices
        self.choices = page_choices
        widgets = (Select(choices=site_choices ),
                   Select(choices=[('', '----')]),
                   Select(choices=self.choices, attrs={'style': "display:none;"} ),
        )
        super(PageSelectWidget, self).__init__(widgets, attrs)
    
    def decompress(self, value):
        """
        receives a page_id in value and returns the site_id and page_id
        of that page or the current site_id and None if no page_id is given.
        """
        if value:
            page = Page.objects.get(pk=value)
            site = page.site
            return [site.pk, page.pk, page.pk]
        site = Site.objects.get_current()
        return [site.pk,None,None]
    
    def _has_changed(self, initial, data):
        # THIS IS A COPY OF django.forms.widgets.Widget._has_changed()
        # (except for the first if statement)
        
        """
        Return True if data differs from initial.
        """
        # For purposes of seeing whether something has changed, None is
        # the same as an empty string, if the data or inital value we get
        # is None, replace it w/ u''.
        if data is None or (len(data)>=2 and data[1] in [None,'']):
            data_value = u''
        else:
            data_value = data
        if initial is None:
            initial_value = u''
        else:
            initial_value = initial
        if force_unicode(initial_value) != force_unicode(data_value):
            return True
        return False
    
    def render(self, name, value, attrs=None):
        # THIS IS A COPY OF django.forms.widgets.MultiWidget.render()
        # (except for the last line)
        
        # value is a list of values, each corresponding to a widget
        # in self.widgets.
        if not isinstance(value, list):
            value = self.decompress(value)
        output = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id', None)
        for i, widget in enumerate(self.widgets):
            try:
                widget_value = value[i]
            except IndexError:
                widget_value = None
            if id_:
                final_attrs = dict(final_attrs, id='%s_%s' % (id_, i))
            output.append(widget.render(name + '_%s' % i, widget_value, final_attrs))
        output.append(r'''<script type="text/javascript">
(function($) {
    var handleSiteChange = function(site_name, selected_id) {
        $("#id_%(name)s_1 optgroup").remove();
        var myOptions = $("#id_%(name)s_2 optgroup[label=" + site_name + "]").clone();
        $("#id_%(name)s_1").append(myOptions);
        $("#id_%(name)s_1").change();
    };
    var handlePageChange = function(page_id) {
        if (page_id) {
            $("#id_%(name)s_2 option").removeAttr('selected');
            $("#id_%(name)s_2 option[value=" + page_id + "]").attr('selected','selected');
        } else {
            $("#id_%(name)s_2 option[value=]").attr('selected','selected');
        };
    };
    $("#id_%(name)s_0").change(function(){
        var site_label = $("#id_%(name)s_0").children(":selected").text();
        handleSiteChange( site_label );
    });
    $("#id_%(name)s_1").change(function(){
        var page_id = $(this).find('option:selected').val();
        handlePageChange( page_id );
    });
    $(function(){
        handleSiteChange( $("#id_%(name)s_0").children(":selected").text() );
        $("#add_id_%(name)s").hide();
    });
})(django.jQuery);
</script>''' % {'name': name})
        return mark_safe(self.format_output(output))
    
    def format_output(self, rendered_widgets):
        return u' '.join(rendered_widgets)
    
    
class PluginEditor(Widget):
    def __init__(self, attrs=None):
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            self.attrs = {}
        
    class Media:
        js = [pathjoin(settings.CMS_MEDIA_URL, path) for path in (
            'js/lib/ui.core.js',
            'js/lib/ui.sortable.js',
            'js/plugin_editor.js',
        )]
        css = {
            'all': [pathjoin(settings.CMS_MEDIA_URL, path) for path in (
                'css/plugin_editor.css',
            )]
        }

    def render(self, name, value, attrs=None):
        
        context = {
            'plugin_list': self.attrs['list'],
            'installed_plugins': self.attrs['installed'],
            'copy_languages': self.attrs['copy_languages'],
            'language': self.attrs['language'],
            'show_copy': self.attrs['show_copy'],
            'placeholder': self.attrs['placeholder'],
        }
        return mark_safe(render_to_string(
            'admin/cms/page/widgets/plugin_editor.html', context))


class UserSelectAdminWidget(Select):
    """Special widget used in page permission inlines, because we have to render
    an add user (plus) icon, but point it somewhere else - to special user creation
    view, which is accessible only if user haves "add user" permissions.
    
    Current user should be assigned to widget in form constructor as an user 
    attribute.
    """
    def render(self, name, value, attrs=None, choices=()):
        output = [super(UserSelectAdminWidget, self).render(name, value, attrs, choices)]    
        if hasattr(self, 'user') and (self.user.is_superuser or \
            self.user.has_perm(PageUser._meta.app_label + '.' + PageUser._meta.get_add_permission())):
            # append + icon
            add_url = '../../../cms/pageuser/add/'
            output.append(u'<a href="%s" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"> ' % \
                    (add_url, name))
            output.append(u'<img src="%simg/admin/icon_addlink.gif" width="10" height="10" alt="%s"/></a>' % (settings.ADMIN_MEDIA_PREFIX, _('Add Another')))
        return mark_safe(u''.join(output))
    
    
class PlaceholderPluginEditorWidget(PluginEditor):
    attrs = {}
    def __init__(self, request, filter_func):
        self.request = request
        self.filter_func = filter_func
            
    def __deepcopy__(self, memo):
        obj = copy.copy(self)
        obj.request = copy.copy(self.request)
        obj.filter_func = self.filter_func
        memo[id(self)] = obj
        return obj
        
    def render(self, name, value, attrs=None):
        try:
            ph = Placeholder.objects.get(pk=value)
        except Placeholder.DoesNotExist:
            ph = None
            context = {'add':True}
        if ph:
            plugin_list = ph.cmsplugin_set.filter(parent=None).order_by('position')
            plugin_list = self.filter_func(self.request, plugin_list)
            language = get_language_from_request(self.request)
            copy_languages = []
            if ph.actions.can_copy:
                copy_languages = ph.actions.get_copy_languages(
                    placeholder=ph,
                    model=ph._get_attached_model(),
                    fieldname=ph._get_attached_field_name()
                )
            context = {
                'plugin_list': plugin_list,
                'installed_plugins': plugin_pool.get_all_plugins(ph.slot),
                'copy_languages': copy_languages, 
                'language': language,
                'show_copy': bool(copy_languages) and ph.actions.can_copy,
                'urloverride': True,
                'placeholder': ph,
            }
        #return mark_safe(render_to_string(
        #    'admin/cms/page/widgets/plugin_editor.html', context))
        return mark_safe(render_to_string(
            'admin/cms/page/widgets/placeholder_editor.html', context, RequestContext(self.request)))

class TextSelect(Widget):
    '''\
    TextInput-like widget providing a Select(Multiple) interface.

    This is actually a COPY of Django's Select widget with some minor
    modifications to make it happy with text, mainly borrowing from
    the TextInput and SelectMultiple class.
    '''

    def __init__(self, attrs=None, choices=(), separator=u','):
        super(TextSelect, self).__init__(attrs)
        # choices can be any iterable, but we may need to render this widget
        # multiple times. Thus, collapse it into a list so it can be consumed
        # more than once.
        # print u'TextSelect ctor: attrs %s, choices %s' % (
        #         str(attrs), str(choices))
        self.choices = list(choices)
        self.separator = separator

    def render(self, name, value, attrs=None, choices=()):
        # print u'TextSelect.render: value %s, choices %s' % (
        #         repr(value), repr(choices))
        # this part is hinted by TextInput...
        if value is None:
            value = ''

        final_attrs = self.build_attrs(attrs, type=u'text', name=name)
        # print u'TextSelect.render: finalattr %s' % (repr(final_attrs), )

        # output = [u'<select%s>' % flatatt(final_attrs)]
        # options = self.render_options(choices, [value])
        # if options:
        #     output.append(options)
        # output.append(u'</select>')
        # return mark_safe(u'\n'.join(output))

        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = self.render_options(choices, value)

        # DEBUG
        # print u'TextSelect.render: <input%s />' % flatatt(final_attrs)
        return mark_safe(u'<input%s />' % flatatt(final_attrs))


    def render_option(self, selected_choices, option_value, option_label):
        # print u'TextSelect option: selected %s, val %s, lbl %s' % (
        #         repr(selected_choices),
        #         repr(option_value),
        #         repr(option_label), )

        option_value = force_unicode(option_value)
        selected = option_value in selected_choices
        if not selected:
            # not selected, don't render this entry
            return None

        # return u'<option value="%s"%s>%s</option>' % (
        #     escape(option_value), selected_html,
        #     conditional_escape(force_unicode(option_label)))
        return conditional_escape(force_unicode(option_label))

    def render_options(self, choices, selected_choices):
        # print u'TextSelect.render_options: self.choices %s' % (
        #         repr(self.choices), )
        # Only render the selected values...

        # Normalize to strings.
        selected_choices = set([force_unicode(v) for v in selected_choices])
        # print u'TextSelect.render_options: selected %s' % (
        #         repr(selected_choices), )

        output = []
        for option_value, option_label in chain(self.choices, choices):
            # print u'TextSelect.render_options: optval:', option_value
            # print u'TextSelect.render_options: optlbl:', option_label

            if isinstance(option_label, (list, tuple)):
                # output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)))
                for option in option_label:
                    entry = self.render_option(selected_choices, *option)

                    if entry is not None:
                        output.append(entry)
                # output.append(u'</optgroup>')
            else:
                entry = self.render_option(selected_choices, option_value, option_label)

                if entry is not None:
                    output.append(entry)


        # print u'TextSelect.render_options: output: %s' % (
        #         self.separator.join(output))
        return self.separator.join(output)

    def value_from_datadict(self, data, files, name):
        if isinstance(data, (MultiValueDict, MergeDict)):
            return data.getlist(name)
        return data.get(name, None)

    def _has_changed(self, initial, data):
        if initial is None:
            initial = []
        if data is None:
            data = []
        if len(initial) != len(data):
            return True
        initial_set = set([force_unicode(value) for value in initial])
        data_set = set([force_unicode(value) for value in data])
        return data_set != initial_set

