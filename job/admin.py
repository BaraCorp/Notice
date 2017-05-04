#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django.contrib import admin
# from django.db import models

# from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from job.forms import (UserChangeForm, UserCreationForm)
from job.models import (Notice, Member, PhoneNumber, Organization,
                        Category, Language)

# unregister and register again
# admin.site.unregister(Group)


@admin.register(Member)
class MemberAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name',
                                      'date_of_birth', 'email',)}),
        ('Permissions', {'fields': ('groups', 'is_admin')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide', 'extrapretty'),
                'fields': ('username', 'password1', 'password2', )}),
        ('Personal info', {'fields': ('first_name', 'image', 'last_name',
                                      'date_of_birth', 'email')}),
        ('Permissions', {'fields': ('groups', 'is_admin')}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class PhoneNumberInline(admin.TabularInline):

    model = PhoneNumber


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):

    list_display = ['name', 'logo', 'date_created', 'capital', 'email',
                    'date_expired', 'is_active']
    list_filter = ['date_created', 'date_expired', 'is_active']
    inlines = [
        PhoneNumberInline,
    ]


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')
    list_filter = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_created', 'share', 'date_expired',
                    'count_view', 'organization', 'slug')
    list_filter = ('date_created', 'date_expired',
                   'organization', 'type_notice')
