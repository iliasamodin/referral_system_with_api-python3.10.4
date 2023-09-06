from django import forms


class PhoneValidationForm(forms.Form):
    phone_number = forms.IntegerField(
        widget=forms.TextInput(attrs={"autofocus": True}),
        # The minimum length of a telephone number in an international entry 
        #   is 10 digits, the maximum is 15
        min_value=1_000_000_000,
        max_value=999_999_999_999_999  
    )


class AuthorizationForm(forms.Form):
    authorization_code = forms.IntegerField(
        label="Code from SMS",
        widget=forms.NumberInput(attrs={"autofocus": True}),
        min_value=1_000,
        max_value=9_999
    )