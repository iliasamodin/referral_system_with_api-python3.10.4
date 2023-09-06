from django import forms


class ReferrerAssignmentFrom(forms.Form):
    referrer_code = forms.CharField(
        widget=forms.TextInput(attrs={"autofocus": True}), 
        min_length=6,
        max_length=6
    )