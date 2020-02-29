from django import forms
from . import models


class EmailMaterialForm(forms.Form):
    name = forms.CharField(max_length=25)
    my_email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False,
                              widget=forms.Textarea)


class MaterialForm(forms.ModelForm):
    class Meta:
        model = models.Material
        fields = ('title', 'body', 'status')

