from django import forms
from django.core import validators


class SuggestionForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    verify_email = forms.EmailField(label="Please verify your email address")
    suggestion = forms.CharField(widget=forms.Textarea)
    poohbear = forms.CharField(required=False, 
                               widget=forms.HiddenInput, 
                               label="Leave empty",
                               validators=[validators.MaxLengthValidator(0)],
                               )


    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        verify = cleaned_data['verify_email']

        if email != verify:
            raise forms.ValidationError(
                "You need to enter the same email in both fields")
