import phonenumbers
from django.forms import ValidationError


class CustomValidations:
    @staticmethod
    def check_phone_number(value):
        try:
            mobile_number = phonenumbers.parse(value)
            if not phonenumbers.is_valid_number(mobile_number):
                raise ValidationError(
                    "The phone number is invalid. Please enter a valid number with the country code."
                )
        except phonenumbers.NumberParseException:
            raise ValidationError(
                "Invalid phone number format. Please include the country code."
            )
