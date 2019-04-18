from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=25)
    from_email = forms.EmailField()
    comment = forms.CharField(required=True, widget=forms.Textarea)
