# -*- coding: utf-8 -*-
from classytags.arguments import IntegerArgument, Argument
from classytags.core import Options
from classytags.helpers import InclusionTag
from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.utils.translation import activate, get_language, ugettext
from menus.menu_pool import menu_pool
import urllib

class NOT_PROVIDED: pass

FILTER_NONE = 0x0000
FILTER_INTER = 0x0001
FILTER_LEAF = 0x0002
FILTER_TRIM_CHILDREN = 0x0010


def cut_after(node, levels, removed):
    """
    given a tree of nodes cuts after N levels
    """
    if levels == 0:
        removed.extend(node.children)
        node.children = []
    else:
        removed_local = []
        for n in node.children:
            if n.visible:
                cut_after(n, levels - 1, removed)
            else:
                removed_local.append(n)
        for n in removed_local:
            node.children.remove(n)
        removed.extend(removed_local)

def remove(node, removed):
    removed.append(node)
    if node.parent:
        if node in node.parent.children:
            node.parent.children.remove(node)

def out_list_unicode(nodes):
    return u'[%s]' % (
            u', '.join(
                u'<%s>: %s' % (
                    node.get_menu_title(),
                    out_list_unicode(node.children),
                    )
                for node in nodes
                )
            )

def out_list(nodes):
    return out_list_unicode(nodes).encode('utf-8')

# def cut_levels(nodes,
#                from_level, to_level, extra_inactive, extra_active,
#                trim_children, debugptr=None, indent_lvl=0,
#                in_travelling=False):
def _do_cut_levels(nodes, from_level, to_level, extra_inactive, extra_active, trim_children, in_travelling):
    """
    cutting nodes away from menus
    """
    final = []
    removed = []
    selected = None

    #fp = open('d:/logs/menudebug.txt', 'a') if debugptr is None else debugptr
    #indent_spaces = '    ' * indent_lvl
    #fp.write('%sPARAM %s %d %d %d %d %s\n' % (indent_spaces, out_list(nodes), 
    #        from_level, to_level, extra_inactive, extra_active, trim_children))
    for node in nodes: 
        #fp.write('%snode: %s:' % (indent_spaces, node.get_menu_title().encode('utf-8')))
        if not hasattr(node, 'level'):
            # remove and ignore nodes that don't have level information
            #fp.write(' NOLVL\n')
            remove(node, removed)
            continue

        #fp.write(' LVL%d' % node.level)
        if node.level == from_level:
            # turn nodes that are on from_level into root nodes
            #fp.write(' ROOT')
            final.append(node)
            # If we are in the recursion of trim_children travel, do not make
            # root to preserve tree structure
            if not in_travelling:
                node.parent = None

        if not node.ancestor and not node.selected and not node.descendant:
            # cut inactive nodes to extra_inactive, but not of descendants of 
            # the selected node
            #fp.write(' INACT')
            cut_after(node, extra_inactive, removed)

        if node.level > to_level and node.parent:
            # remove nodes that are too deep, but not nodes that are on 
            # from_level (local root nodes)
            #fp.write(' DEPTH')
            remove(node, removed)

        # Trim children of the last level??
        if trim_children and len(node.children) > 0:
            if node.level == to_level:
                #fp.write(' DOTRIM: %s' % repr(node.children))
                node.children = []
            else:
                # recurse!
                #fp.write(' TRIMTRAVEL\n')
                #fp.flush()
                node.children = _do_cut_levels(node.children, from_level + 1, to_level,
                        extra_inactive, extra_active,
                        trim_children, True
                        )

        if node.selected:
            selected = node

        if not node.visible:
            remove(node, removed)
        #fp.write('\n')

    if selected:
        cut_after(selected, extra_active, removed)
    if removed:
        for node in removed:
            if node in final:
                final.remove(node)
    #fp.write('%sAFTER: %s\n' % (indent_spaces, out_list(final)))
    #if debugptr is None:
    #    fp.close()
    return final

def cut_levels(nodes, from_level, to_level, extra_inactive, extra_active, trim_children):
    return _do_cut_levels(nodes, from_level, to_level, extra_inactive, extra_active, trim_children, False)

register = template.Library()

class ShowMenuBaseMixin(object):
    def _get_context_internal(self, context, from_level, to_level, extra_inactive,
                    extra_active, max_count, filter_opt, template, namespace, root_id, next_page):
        trim_children = (filter_opt & FILTER_TRIM_CHILDREN != 0)
        try:
            # If there's an exception (500), default context_processors may not be called.
            request = context['request']
        except KeyError:
            return {'template': 'menu/empty.html'}

        has_root_node = False

        if next_page:
            children = next_page.children
        else: 
            #new menu... get all the data so we can save a lot of queries
            nodes = menu_pool.get_nodes(request, namespace, root_id)
            if root_id: # find the root id and cut the nodes
                id_nodes = menu_pool.get_nodes_by_attribute(nodes, "reverse_id", root_id)
                if id_nodes:
                    root_node = node = id_nodes[0]
                    has_root_node = True

                    new_nodes = node.children
                    for n in new_nodes:
                        n.parent = None
                    from_level += node.level + 1
                    to_level += node.level + 1
                else:
                    new_nodes = []
                nodes = new_nodes
            children = cut_levels(nodes, from_level, to_level, extra_inactive, extra_active, trim_children)
            children = menu_pool.apply_modifiers(children, request, namespace, root_id, post_cut=True)

        if filter_opt & FILTER_INTER:
            children = [node for node in children if node.is_leaf_node]
        elif filter_opt & FILTER_LEAF:
            children = [node for node in children if not node.is_leaf_node]

        # only return the top ``max_count`` ones if specified
        if max_count != -1:
            children = children[:max_count]

        try:
            context.update({'children':children,
                            'template':template,
                            'from_level':from_level,
                            'to_level':to_level,
                            'extra_inactive':extra_inactive,
                            'extra_active':extra_active,
                            'max_count':max_count,
                            'filter_opt':filter_opt,
                            'namespace':namespace})
            if has_root_node:
                context['root_node'] = root_node

        except:
            context = {"template":template}
        return context


class ShowMenu(InclusionTag, ShowMenuBaseMixin):
    """
    render a nested list of all children of the pages
    - from_level: starting level
    - to_level: max level
    - extra_inactive: how many levels should be rendered of the not active tree?
    - extra_active: how deep should the children of the active node be rendered?
    - namespace: the namespace of the menu. if empty will use all namespaces
    - root_id: the id of the root node
    - template: template used to render the menu
    """
    name = 'show_menu'
    template = 'menu/dummy.html'

    options = Options(
        IntegerArgument('from_level', default=0, required=False),
        IntegerArgument('to_level', default=100, required=False),
        IntegerArgument('extra_inactive', default=0, required=False),
        IntegerArgument('extra_active', default=1000, required=False),
        # Count support...
        IntegerArgument('max_count', default=-1, required=False),
        IntegerArgument('filter_opt', default=FILTER_NONE, required=False),
        Argument('template', default='menu/menu.html', required=False),
        Argument('namespace', default=None, required=False),
        Argument('root_id', default=None, required=False),
        Argument('next_page', default=None, required=False),
    )
    
    def get_context(self, context, from_level, to_level, extra_inactive,
            extra_active, max_count, filter_opt, template, namespace, root_id, next_page):
        return ShowMenuBaseMixin._get_context_internal(self, context,
                from_level, to_level, extra_inactive, extra_active, max_count, filter_opt,
                template, namespace, root_id, next_page)

register.tag(ShowMenu)


class ShowMenuBelowId(ShowMenu):
    name = 'show_menu_below_id'
    options = Options(
        Argument('root_id', default=None, required=False),
        IntegerArgument('from_level', default=0, required=False),
        IntegerArgument('to_level', default=100, required=False),
        IntegerArgument('extra_inactive', default=0, required=False),
        IntegerArgument('extra_active', default=1000, required=False),
        # Count support...
        IntegerArgument('max_count', default=-1, required=False),
        IntegerArgument('filter_opt', default=FILTER_NONE, required=False),
        Argument('template', default='menu/menu.html', required=False),
        Argument('namespace', default=None, required=False),
        Argument('next_page', default=None, required=False),
    )
register.tag(ShowMenuBelowId)


########################################################################

class ShowSubMenu(InclusionTag):
    """
    show the sub menu of the current nav-node.
    -levels: how many levels deep
    -temlplate: template used to render the navigation
    """
    name = 'show_sub_menu'
    template = 'menu/dummy.html'
    
    options = Options(
        IntegerArgument('levels', default=100, required=False),
        Argument('template', default='menu/sub_menu.html', required=False),
    )
    
    def get_context(self, context, levels, template):
        try:
            # If there's an exception (500), default context_processors may not be called.
            request = context['request']
        except KeyError:
            return {'template': 'menu/empty.html'}
        nodes = menu_pool.get_nodes(request)
        children = []
        for node in nodes:
            if node.selected:
                cut_after(node, levels, [])
                children = node.children
                for child in children:
                    child.parent = None
                children = menu_pool.apply_modifiers(children, request, post_cut=True)
        context.update({
            'children':children,
            'template':template,
            'from_level':0,
            'to_level':0,
            'extra_inactive':0,
            'extra_active':0
        })
        return context        
register.tag(ShowSubMenu)


class ShowBreadcrumb(InclusionTag):
    """
    Shows the breadcrumb from the node that has the same url as the current request
    
    - start level: after which level should the breadcrumb start? 0=home
    - template: template used to render the breadcrumb 
    """
    name = 'show_breadcrumb'
    template = 'menu/dummy.html'
    
    options = Options(
        Argument('start_level', default=0, required=False),
        Argument('template', default='menu/breadcrumb.html', required=False),
        Argument('only_visible', default=True, required=False),
    )

    def get_context(self, context, start_level, template, only_visible):
        try:
            # If there's an exception (500), default context_processors may not be called.
            request = context['request']
        except KeyError:
            return {'template': 'cms/content.html'}
        if not (isinstance(start_level, int) or start_level.isdigit()):
            only_visible = template
            template = start_level
            start_level = 0
        try:
            only_visible = bool(int(only_visible))
        except:
            only_visible = bool(only_visible)
        ancestors = []
        nodes = menu_pool.get_nodes(request, breadcrumb=True)
        selected = None
        home = None
        for node in nodes:
            if node.selected:
                selected = node
            if node.get_absolute_url() == urllib.unquote(reverse("pages-root")):
                home = node
        if selected and selected != home:
            n = selected
            while n:
                if n.visible or not only_visible:
                    ancestors.append(n)
                n = n.parent
        if not ancestors or (ancestors and ancestors[-1] != home) and home:
            ancestors.append(home)
        ancestors.reverse()
        if len(ancestors) >= start_level:
            ancestors = ancestors[start_level:]
        else:
            ancestors = []
        context.update({'ancestors':ancestors,
                        'template': template})
        return context
register.tag(ShowBreadcrumb)


def _raw_language_marker(language, lang_code):
    return language

def _native_language_marker(language, lang_code):
    activate(lang_code)
    return unicode(ugettext(language))

def _current_language_marker(language, lang_code):
    return unicode(ugettext(language))

def _short_language_marker(language, lang_code):
    return lang_code

MARKERS = {
    'raw': _raw_language_marker,
    'native': _native_language_marker,
    'current': _current_language_marker,
    'short': _short_language_marker,
}

class LanguageChooser(InclusionTag):
    """
    Displays a language chooser
    - template: template used to render the language chooser
    """
    name = 'language_chooser'
    template = 'menu/dummy.html'
    
    options = Options(
        Argument('template', default=NOT_PROVIDED, required=False),
        Argument('i18n_mode', default='raw', required=False),
    )

    def get_context(self, context, template, i18n_mode):
        if template in MARKERS:
            _tmp = template
            if i18n_mode not in MARKERS:
                template = i18n_mode
            else:
                template = NOT_PROVIDED
            i18n_mode = _tmp
        if template is NOT_PROVIDED:
            template = "menu/language_chooser.html"
        if not i18n_mode in MARKERS:
            i18n_mode = 'raw'
        if 'request' not in context:
            # If there's an exception (500), default context_processors may not be called.
            return {'template': 'cms/content.html'}
        marker = MARKERS[i18n_mode]
        cms_languages = dict(settings.CMS_LANGUAGES)
        current_lang = get_language()
        site = Site.objects.get_current()
        site_languages = settings.CMS_SITE_LANGUAGES.get(site.pk, cms_languages.keys())
        cache_key = '%s-language-chooser-%s-%s-%s' % (settings.CMS_CACHE_PREFIX, site.pk, current_lang, i18n_mode)
        languages = cache.get(cache_key, [])
        if not languages:
            for lang in settings.CMS_FRONTEND_LANGUAGES:
                if lang in cms_languages and lang in site_languages:
                    languages.append((lang, marker(cms_languages[lang], lang)))
            if current_lang != get_language():
                activate(current_lang)
            cache.set(cache_key, languages)
        lang = get_language()
        context.update({
            'languages':languages,
            'current_language':lang,
            'template':template,
        })
        return context
register.tag(LanguageChooser)


class PageLanguageUrl(InclusionTag):
    """
    Displays the url of the current page in the defined language.
    You can set a language_changer function with the set_language_changer function in the utils.py if there is no page.
    This is needed if you have slugs in more than one language.
    """
    name = 'page_language_url'
    template = 'cms/content.html'
    
    options = Options(
        Argument('lang'),
    )
    
    def get_context(self, context, lang):
        try:
            # If there's an exception (500), default context_processors may not be called.
            request = context['request']
        except KeyError:
            return {'template': 'cms/content.html'}
        if hasattr(request, "_language_changer"):
            try:
                setattr(request._language_changer, 'request', request)
            except AttributeError:
                pass
            url = "/%s" % lang + request._language_changer(lang)
        else:
            page = request.current_page
            if page == "dummy":
                return ''
            try:
                url = page.get_absolute_url(language=lang, fallback=False)
                url = "/" + lang + url
            except:
                # no localized path/slug. 
                url = ''
        return {'content':url}
register.tag(PageLanguageUrl)
