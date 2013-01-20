# -*- coding: utf-8 -*-
#
# written mainly for the tags -- text-based ModelMultipleChoiceField

from django.core.exceptions import ValidationError, FieldError
from django.utils.encoding import smart_unicode, force_unicode

from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from django.forms.widgets import HiddenInput, MultipleHiddenInput
from django.utils.translation import ugettext_lazy as _

# homebrew Select(Multiple)-TextInput hybrid
from cms.forms.widgets import TextSelect

# Default separator used
DEFAULT_SEPARATOR = u','

class TextModelMultipleChoiceField(ModelChoiceField):
    """
    A text-based ModelMultipleChoiceField.
    """

    widget = TextSelect
    hidden_widget = MultipleHiddenInput
    default_error_messages = {
        'list': _(u'Enter a list of values.'),
        'invalid_choice': _(u'Select a valid choice. %s is not one of the'
                            u' available choices.'),
        'invalid_pk_value': _(u'"%s" is not a valid value for a primary key.')
    }

    def __init__(self, queryset, cache_choices=False, required=True,
                 widget=None, label=None, initial=None,
                 help_text=None, separator=DEFAULT_SEPARATOR, *args, **kwargs):
        super(TextModelMultipleChoiceField, self).__init__(queryset, None,
            cache_choices, required, widget, label, initial, help_text,
            *args, **kwargs)

        self.separator = separator

    # the prop is for appropriate syncing with widget
    def _get_separator(self):
        return self._separator

    def _set_separator(self, new_separator):
        self._separator = self.widget.separator = new_separator

    separator = property(_get_separator, _set_separator)

    def clean(self, value):
        # This field's reason for existing is just enabling quick tag edit, so
        # no matching against some "choices" is done.
        # NOTE: Saving happens in PageAdmin.save_model()

        # XXX eh... why is value a one-item list?
        value = value[0]

        # Some sanity checking is still required...
        # print u'Text.M.M.C.Field: clean: value "%s"' % value
        if self.required and not value:
            raise ValidationError(self.error_messages['required'])
        if not isinstance(value, unicode):
            # FIXME: i18n
            raise ValidationError(self.error_messages['list'])

        # Just return the "raw" Unicode choice string.
        return value

    def prepare_value(self, value):
        if hasattr(value, '__iter__'):
            return [super(TextModelMultipleChoiceField, self).prepare_value(v) for v in value]
        return super(TextModelMultipleChoiceField, self).prepare_value(value)

