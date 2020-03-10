from django import forms
from . import models
from django.contrib.auth.models import User


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


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('name', 'email', 'body')


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Pass',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='repeat',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('bad pass')
        return cd['password2']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ('birth', 'photo')


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

