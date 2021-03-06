# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from captcha.fields import CaptchaField

from .models import User


class RegistrationForm(forms.ModelForm):
    """ User registration form. """

    error_css_class = 'error'
    username = forms.CharField(widget=forms.TextInput, label="Login")
    password1 = forms.CharField(widget=forms.PasswordInput,
                                min_length=6, max_length=16, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput,
                                min_length=6, max_length=16,
                                label="Confirm password")
    email = forms.CharField(widget=forms.TextInput, label="E-mail")
    birth_date = forms.DateField(widget=forms.TextInput, label="Birth date")
    first_name = forms.CharField(widget=forms.TextInput, label="Name")
    last_name = forms.CharField(widget=forms.TextInput, label="Surname")
    phone = forms.RegexField(regex=r'^0\d{2}-\d{7}$',
                             error_messages={'invalid':
                                             "Pattern: 0xx-xxxxxxx"})
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'username',
                  'password1', 'password2', 'email',
                  'birth_date', 'phone']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        if 'password1' in cleaned_data and \
           'password2' in cleaned_data:
            if cleaned_data['password1'] != \
               cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match.")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class AuthenticationForm(forms.Form):
    """ User authenticate form. """

    error_messages = {
        'invalid_login': "Please enter a correct username and password.",
        'inactive': "This account is inactive."}
    username = forms.CharField(widget=forms.TextInput, label="Login",
                               error_messages={'required':
                                               'Please enter your name'})
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        fields = ['username', 'password']

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in.
        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )


class EditForm(forms.ModelForm):
    """ User edit form based on model fields. """

    password = forms.CharField(widget=forms.PasswordInput,
                               min_length=6, max_length=16, label="Password")
    # picture = forms.CharField(widget=forms.FileInput(attrs={'id': 'image'}))
    # picture = forms.CharField(widget=forms.ClearableFileInput(
    #    attrs={'accept':'photos/', 'upload_to': 'photos/'}))
    # picture.widget.attrs['id'] = 'test'

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'username', 'password', 'email',
                  'birth_date', 'phone', 'picture']

    def save(self, commit=True):
        user = super(EditForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
