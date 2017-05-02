#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django.conf import settings
# from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse

from job.models import Notice, Member, Organization
from job.forms import (SearchForm, UserCreationForm, NewNoticeForm,
                       UserChangeForm, NewOrganizationForm)


def init(request):

    search_form = SearchForm(request.POST or None)
    result = ""
    result_not_found = ""
    if request.method == 'POST' and '_search' in request.POST:
        print("search")
        if search_form.is_valid():
            result = search_form.get_result('number_engin')
            if not result:
                result_not_found = "Aucun numéro ne correspond"

    context = {'user': request.user,
               'result_not_found': result_not_found,
               'search_form': search_form, 'msg_result': result,
               'settings': settings}
    return context


@login_required
def add_notice(request, *args, **kwargs):
    id_url = kwargs["pk_org"]

    orgztion = Organization.objects.get(pk=id_url)
    user = request.user
    if request.method == 'POST' and '_new_notice' in request.POST:
        notice_form = NewNoticeForm(request.POST or None)
        if notice_form.is_valid():
            notice = notice_form.save(commit=False)
            notice.organization = orgztion
            notice.save()
            return redirect("/")
    else:
        notice_form = NewNoticeForm()
    cxt = {'user': user, 'notice_form': notice_form,
           'org_name': orgztion.name}
    return render(request, 'new_notice.html', cxt)


@login_required
def notice_change(request, *args, **kwargs):
    id_url = kwargs["pk_notice"]
    cxt = {}
    return render(request, 'new_notice.html', cxt)


@login_required
def notice_view(request, *args, **kwargs):
    id_url = kwargs["pk_notice"]
    notice = Notice.objects.get(pk=id_url)
    cxt = {'notice': notice}
    return render(request, 'notice_view.html', cxt)


@login_required
def user_manager(request):
    members = Member.objects.filter(is_admin=False)

    for member in members:
        member.url_change = reverse("user-change", args=[member.pk])

    user = request.user
    if request.method == 'POST' and '_new_notice' in request.POST:
        notice_form = NewNoticeForm(request.POST or None)
        if notice_form.is_valid():
            # notice = notice_form.save(commit=False)
            # notice.author = Member.objects.filter()
            # notice.save()
            return redirect("/")
    else:
        notice_form = NewNoticeForm()
    cxt = {'members': members, 'user': user, 'notice_form': notice_form}
    return render(request, 'user_manager.html', cxt)


@login_required
def new_user(request):
    if request.method == 'POST' and '_new_user' in request.POST:
        new_user_form = UserCreationForm(request.POST or None)
        if new_user_form.is_valid():
            new_user_form.save()
            return redirect("/home")
    else:
        new_user_form = UserCreationForm()
    cxt = {"new_user_form": new_user_form}
    return render(request, 'new_user.html', cxt)


@login_required
def user_change(request, *args, **kwargs):
    id_url = kwargs["pk"]

    selected_member = Member.objects.get(pk=id_url)
    print(selected_member)
    if request.method == 'POST' and 'user_change' in request.POST:
        user_change_form = UserChangeForm(request.POST,
                                          instance=selected_member)
        if user_change_form.is_valid():
            user_change_form.save()
            return redirect("/user-manager")
    else:
        user_change_form = UserChangeForm(instance=selected_member)
    cxt = {"new_user_form": user_change_form}
    return render(request, 'new_user.html', cxt)


@login_required
def organization_manager(request):
    organizations = Organization.objects.filter(is_active=True)
    for organization in organizations:
        organization.url_change = reverse(
            "organization-change", args=[organization.pk])
        organization.url_view = reverse(
            "organization-view", args=[organization.pk])
        organization.url_notice = reverse(
            "add-notice", args=[organization.pk])

    user = request.user
    if request.method == 'POST' and '_new_organization' in request.POST:
        org_form = NewOrganizationForm(request.POST or None)
        if org_form.is_valid():
            # notice = org_form.save(commit=False)
            # notice.author = Member.objects.filter()
            # notice.save()
            return redirect("/")
    else:
        org_form = NewOrganizationForm()
    cxt = {'organizations': organizations, 'user': user,
           'org_form': org_form}
    return render(request, 'organization_manager.html', cxt)


@login_required
def organization_view(request, *args, **kwargs):
    id_url = kwargs["pk"]
    org = Organization.objects.get(pk=id_url)
    notices = Notice.objects.filter(organization=org)
    for notice in notices:
        notice.url_view = reverse("notice-view", args=[notice.pk])
        notice.url_change = reverse("notice-change", args=[notice.pk])
    cxt = {'notices': notices, "id_url": id_url}
    return render(request, 'organization_view.html', cxt)


@login_required
def organization_change(request, *args, **kwargs):
    id_url = kwargs["pk"]

    selected_organization = Organization.objects.get(pk=id_url)
    if request.method == 'POST' and '_new_organization' in request.POST:
        organization_change_form = NewOrganizationForm(
            request.POST, instance=selected_organization)
        if organization_change_form.is_valid():
            organization_change_form.save()
            return redirect("/organization_manager")
    else:
        organization_change_form = NewOrganizationForm(
            instance=selected_organization)
    cxt = {"new_organization_form": organization_change_form}
    return render(request, 'new_organization.html', cxt)


@login_required
def new_organization(request):
    if request.method == 'POST' and '_new_organization' in request.POST:
        new_org_form = NewOrganizationForm(request.POST, request.FILES)
        print("login")
        if new_org_form.is_valid():
            new_org_form.save()
            return redirect("/organization_manager")
    else:
        new_org_form = NewOrganizationForm()
    cxt = {"new_organization_form": new_org_form}
    return render(request, 'new_organization.html', cxt)


def index(request):

    cxt = init(request)
    notices = Notice.objects.all()
    # import ipdb; ipdb.set_trace()
    cxt.update({'notices': notices})
    return render(request, 'index.html', cxt)


def home(request):

    cxt = init(request)
    notices = Notice.objects.all()
    cxt.update({'notices': notices})
    return render(request, 'home.html', cxt)
