from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator


class LenPhoneValidator(BaseValidator):
    def clean(self, x):
        return len(str(x))


def validate_first_num_phone(value):
    if str(value)[0] != '7':
        raise ValidationError('Ensure this value starts with 7')
