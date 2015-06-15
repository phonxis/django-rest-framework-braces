from __future__ import print_function, unicode_literals

import six

from . import _fields as fields
from .mixins import EmptyStringFieldMixing, ValueAsTextFieldMixin


class UnvalidatedField(fields._UnvalidatedField):
    """
    Same as DRF's ``_UnvalidatedField``, except this is a public class.
    """


class PositiveIntegerField(fields.IntegerField):
    """
    Enhanced DRF's ``IntegerField`` as this default ``min_value`` to be 0
    hence only allowing positive numbers.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('min_value', 0)
        super(PositiveIntegerField, self).__init__(*args, **kwargs)


class NonValidatingChoiceField(EmptyStringFieldMixing, fields.ChoiceField):
    """
    ChoiceField subclass that skips the validation of "choices".
    It does apply 'required' validation, and any other validation
    done by the parent drf.Field class.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('choices', [])
        super(NonValidatingChoiceField, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        try:
            return self.choice_strings_to_values[six.text_type(data)]
        except KeyError:
            return six.text_type(data)


class NumericField(ValueAsTextFieldMixin, EmptyStringFieldMixing, fields.IntegerField):
    default_error_messages = {
        'invalid': _('Enter a whole number.'),
    }


__all__ = [name for name, value in locals().items() if issubclass(value, fields.Field)]
