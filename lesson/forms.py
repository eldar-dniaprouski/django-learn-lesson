from django import forms


class EmailMaterialForm(forms.Form):
    name = forms.CharField(max_length=25)
    my_email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False,
                              widget=forms.Textarea)
