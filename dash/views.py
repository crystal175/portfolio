# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.urlresolvers import reverse

from .models import User
from .forms import AuthenticationForm, RegistrationForm, EditForm


def main(request):
    """ Main page view. """
    return render(request, 'main.html')


def contacts(request):
    """ Contacts page view. """
    return render(request, 'contacts.html')


def login_user(request):
    """ User login view. """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'mylogin.html')
    else:
        form = AuthenticationForm()
    return render_to_response('mylogin.html', {'form': form},
                              context_instance=RequestContext(request))


def register(request):
    """ User registration view. """
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            subject = 'Registration on site'
            from_email = ''
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            message = u'You registered with nickname - %s' % username
            send_mail(subject, message, from_email, [email])
            human = True
            form.save()
            return redirect(reverse('dash:login'))
    else:
        form = RegistrationForm()
    return render_to_response('myregister.html', {'form': form},
                              context_instance=RequestContext(request))


@login_required
def logout_user(request):
    """ User logout view. """
    logout(request)
    return redirect(reverse('dash:main'))


@login_required
def edit_user(request):
    """ User edit view. """
    user = request.user
    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            picture = form.cleaned_data.get('picture')
            usr = User.objects.get(username=username)
            usr.picture = picture
            form.save()
            return redirect(reverse('dash:login'))
    else:
        form = EditForm(instance=user)
    return render(request, 'edit_user.html', {'form': form})


@login_required
def delete_user(request):
    """ Delete user account view. """
    usr = User.objects.get(username=request.user)
    usr.delete()
    return redirect(reverse('dash:main'))
