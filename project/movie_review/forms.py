from django import forms


class SuggestionForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    suggestion = forms.CharField(widget=forms.Textarea)
    poohbear = forms.CharField(required=False, 
                               widget=forms.HiddenInput, 
                               label="Leave empty")

    def clean_poohbear(self):
        poohbear = self.cleaned_data['poohbear']
        if len(poohbear):
            raise forms.ValidationError(
                "poohbear field should be left empty. Bad bot!")
        return poohbear

