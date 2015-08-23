# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user class. """

    username = models.CharField(max_length=30, unique=True,
                                db_index=True, verbose_name="Login")
    first_name = models.CharField(max_length=30, blank=True,
                                  verbose_name="Name")
    last_name = models.CharField(max_length=30, blank=True,
                                 verbose_name="Surname")
    email = models.EmailField(blank=True, unique=True, db_index=True,
                              verbose_name="E-mail")
    birth_date = models.DateField(auto_now=False, verbose_name="Birth date")
    joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    phone = models.CharField(max_length=12, blank=True,
                             verbose_name="Phone")
    picture = models.ImageField(upload_to='photos/',
                                default='photos/def.jpeg',
                                verbose_name='Avatar')
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    def __unicode__(self):
        return self.username

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name
