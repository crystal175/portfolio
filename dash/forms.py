# -*- coding: utf-8 -*-

from django import forms
from dash.models import User

from captcha.fields import CaptchaField
from django.contrib.auth import authenticate


class RegistrationForm(forms.ModelForm):
    """
    User registration view.
    """

    error_css_class = 'error'

    username = forms.CharField(widget=forms.TextInput,
                                label="Логин")
    password1 = forms.CharField(widget=forms.PasswordInput,
                                min_length=6, max_length=16,
                                label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput,
                                min_length=6, max_length=16,
                                label="Подтвердите пароль")
    email = forms.CharField(widget=forms.TextInput,
                                label="E-mail")
    birth_date = forms.DateField(widget=forms.TextInput,
                                label="Дата рождения")
    first_name = forms.CharField(widget=forms.TextInput,
                                label="Имя")
    last_name = forms.CharField(widget=forms.TextInput,
                                label="Фамилия")
    phone = forms.RegexField(regex=r'^0\d{2}-\d{7}$',
                            error_messages = {'invalid':
                            "Неверный формат. Пример: 0xx-xxxxxxx"} )
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = [ 'last_name', 'first_name', 'username',
                    'password1', 'password2', 'email',
                    'birth_date', 'phone' ]

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match.")
        # if len(self.cleaned_data['password1']) < 7:
        #   self.add_error('password1', 'short password')

        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class AuthenticationForm(forms.Form):
    """
    User authenticate form.
    """

    error_messages = {
        'invalid_login': "Please enter a correct username and password. ",
        'inactive': "This account is inactive.",}

    username = forms.CharField(widget=forms.TextInput,
                                label="Логин",
                                error_messages={'required': 'Please enter your name'},
                                # help_text='must be unique'
                                )
    password = forms.CharField(widget=forms.PasswordInput,
                                label="Пароль")

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
                    # code='invalid_login',
                    # params={'username': username},
                    )
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.
        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.
        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )


class EditForm(forms.ModelForm):
    """
    User edit form.
    """
    password = forms.CharField(widget=forms.PasswordInput,
                                min_length=6, max_length=16,
                                label="Пароль")
    #picture = forms.CharField(widget=forms.FileInput(attrs={'id': 'image'}))
    #picture = forms.CharField(widget=forms.ClearableFileInput(attrs={'accept':'photos/', 'upload_to': 'photos/'}))
    #picture.widget.attrs['id'] = 'test'

    class Meta:
        model = User
        fields = [ 'last_name', 'first_name', 'username',
                    'password', 'email', 'birth_date',
                    'phone', 'picture' ]

    def clean(self):
        cleaned_data = super(EditForm, self).clean()
        return self.cleaned_data

    def save(self, commit=True):
        user = super(EditForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


