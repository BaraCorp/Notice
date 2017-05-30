#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from tinymce.widgets import TinyMCE
# from django.utils.translation import ugettext_lazy as _

from functools import partial

from job.models import (Member, Notice, Organization, SmallNotice)


class SearchForm(forms.Form):

    number_engin = forms.CharField(
        label="Numéro de l'engins", max_length=200, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'recherche par numéro'}),)

    def get_result(self, required):
        try:
            result = Notice.objects.get(
                number=self.cleaned_data.get('number_engin'))
        except Exception:
            result = None
        return result


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError(
                "Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


class NewOrganizationForm(forms.ModelForm):
    DateInput = partial(forms.DateInput, {'class': 'datepicker'})

    class Meta:
        model = Organization
        fields = ('name', 'logo', 'date_created', 'capital',
                  'email', 'date_expired', 'is_active')
        exclude = ['date_joined']
        widgets = {'date_created': forms.DateInput(
            attrs={'class': 'datepicker'})}


class NewNoticeForm(forms.ModelForm):

    body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Notice

        # fields = ('type_notice', 'title', 'share',
        #           'date_expired')
        exclude = ['organization', 'slug', 'date_created', 'count_view']


class UserCreationForm(forms.ModelForm):
    """ A form for creating new users. Includes all the required fields, plus a
        repeated password.
    """

    class Meta:
        model = Member
        fields = ('username', 'image', 'date_of_birth', 'full_name', 'email',
                  'localite')
        # exclude = ['email']

        widgets = {
            # 'date_of_birth': forms.DateInput(attrs={'class': 'datepicker'}),
            'full_name': forms.TextInput(attrs={
                'placeholder': "Nom et prénom"}),
            'localite': forms.TextInput(attrs={
                'placeholder': "Adresse"}),
            # 'date_of_birth': forms.TextInput(
            #     attrs={'placeholder': "Date", 'class': 'datepicker'}),
        }

    username = forms.CharField(max_length=255, required=True)
    full_name = forms.CharField(max_length=200)
    # date_of_birth = forms.DateField(label="Date de naissance")
    localite = forms.CharField(max_length=100)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Member
        # fields = (
        #     'email', 'password', 'date_of_birth', 'is_active', 'is_admin')
        exclude = ['is_admin']

    def clean_password(self):
        return self.initial["password"]


class SmallNoticeForm(forms.ModelForm):
    """docstring for SmallNoticeForm"""

    class Meta:
        model = SmallNotice
        # fields = (
        #     'email', 'password', 'date_of_birth', 'is_active', 'is_admin')
        exclude = ['count_view', 'date']

        widgets = {
            # 'date_of_birth': forms.DateInput(attrs={'class': 'datepicker'}),
            'name': forms.TextInput(attrs={
                'placeholder': "Nom et prénom"}),
            'email': forms.TextInput(attrs={
                'placeholder': "Adresse e-mail"}),
            'subject': forms.TextInput(attrs={
                'placeholder': "Sujet"}),
            'body': forms.Textarea(attrs={
                'placeholder': 'Message en 120 caractères.'}),
        }
