# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail

from models import User
from dash.forms import AuthenticationForm, RegistrationForm, EditForm


def main(request):
    return render(request, 'main.html')

def contacts(request):
    """
    Coantacts page view.
    """
    return render(request, 'contacts.html')

def load_data(request):
    """
    Test view
    """
    usr = User.objects.all()
    return render(request, 'load_data.html', { 'usr': usr })

####################################

def login_user(request):
    """
    Log in view
    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'mylogin.html')
    else:
        form = AuthenticationForm()
    return render_to_response('mylogin.html', {
        'form': form,
    }, context_instance=RequestContext(request))


def register(request):
    """
    User registration view.
    """
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            subject = 'Регистрация на сайте'
            from_email = 'crystal-man@list.ru'
            username=request.POST['username']
            email=request.POST['email']          
            message = u'Вы зарегистрировались под ником - %s' % username
            send_mail(subject, message, from_email, [email])
            
            human = True
            user = form.save()
            return redirect('/dash/login/')
    else:
        form = RegistrationForm()
    return render_to_response('myregister.html', {
        'form': form,
    }, context_instance=RequestContext(request))



def logout_user(request):
    """
    Log out view.
    """
    logout(request)
    return redirect('/')   


def edit_user(request):
    """
    User edit view.
    """
    user = request.user
    
    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            m = User.objects.get(username=form.cleaned_data['username'])
            m.picture  = form.cleaned_data['picture']
            form.save()
            return redirect('/dash/login/')
    else:
        form = EditForm(instance=user)
    return render(request, 'edit_user.html', {'form': form})


def delete_user(request):
    """
    Delete user account.
    """
    m = User.objects.get(username=request.user)
    m.delete()
    return redirect('/')