#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import os
import re

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.core import validators

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField


class MemberManager(BaseUserManager):
    def create_user(self, email, username, date_of_birth=None,
                    password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an username')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            # date_of_birth=date_of_birth,
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password,
                         email=None, date_of_birth=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            # date_of_birth=date_of_birth,
            username=username,
        )
        user.is_admin = True
        user.is_active = True
        # user.has_perm = True
        user.save(using=self._db)
        return user


class Language(models.Model):

    FR = "fr"
    EN = "en"
    AR = "ar"
    LANGUAGES_CHOICES = {
        FR: _('French'),
        EN: _('English'),
        AR: _('Arabic'),
    }

    slug = models.SlugField(max_length=50, verbose_name=_("Slug"),
                            choices=LANGUAGES_CHOICES.items())
    name = models.CharField(max_length=100, blank=True, null=True,
                            verbose_name=_("Name"))

    def __str__(self):
        return u"({slug}) {name}".format(name=self.name, slug=self.slug)


class Member(AbstractBaseUser, PermissionsMixin):

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    username = models.CharField(
        _("username"), max_length=50, primary_key=True,
        help_text=_("Required. 50 characters or fewer. "
                    "Letters, numbers and @/./+/-/_ characters"),
        validators=[validators.RegexValidator(re.compile("^[\w.@+-]+$"),
                                              _("Enter a valid username."),
                                              "invalid")])

    first_name = models.CharField(max_length=100, blank=True, null=True,
                                  verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, blank=True, null=True,
                                 verbose_name=_("Last Name"))
    image = models.ImageField(upload_to='images_member/', blank=True,
                              verbose_name=_("Photo"))
    email = models.EmailField(_("email address"), blank=True, null=True)
    is_staff = models.BooleanField(_("staff status"), default=False,
                                   help_text=_(
        "Designates whether the user can log into this admin site."))
    is_active = models.BooleanField(
        _("active"), default=True,
        help_text=_("Designates whether this user should be treated as "
                    "active. Unselect this instead of deleting accounts."))
    date_of_birth = models.DateField(
        blank=True, null=True, default=timezone.now)
    is_admin = models.BooleanField(default=False)
    objects = MemberManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.name()

    def get_short_name(self):
        return self.name()

    def name(self):
        if not self.first_name and not self.last_name:
            return self.username
        elif not self.first_name:
            return self.last_name
        else:
            return self.first_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Organization(models.Model):
    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")
        ordering = ['-name']

    name = models.CharField(max_length=100, verbose_name=_("Nom"))
    logo = models.ImageField(
        upload_to='media/org_logo/', blank=True, verbose_name=_("Logo"))
    date_joined = models.DateTimeField(
        verbose_name=_("Joined date"), auto_now=True)
    date_created = models.DateTimeField(
        verbose_name=_("Created date"), default=timezone.now)
    capital = models.IntegerField(verbose_name=_("Capital"))
    email = models.EmailField(_("email address"), blank=True, null=True)
    date_expired = models.DateTimeField(
        verbose_name=_("Expired date"), null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return "{}/{}".format(self.name, self.capital)


class PhoneNumber(models.Model):
    organization = models.ForeignKey(
        Organization, verbose_name=_("Organization"))
    type_number = models.CharField(
        max_length=100, verbose_name=_("Type phone number"))
    phone = models.IntegerField(verbose_name=_("Phone n°"))

    def __str__(self):
        return self.phone, self.type_number


class Contract(models.Model):

    class Meta(object):
        verbose_name = _("Contract")
        verbose_name_plural = _("Contracts")

    name = models.CharField(max_length=200, verbose_name=_("Name"))

    def __str__(self):
        return self.name


class SmallNoticeManager(models.Manager):

    def get_queryset(self):
        return super(SmallNoticeManager, self).get_queryset()

    def unreject(self):
        return super(SmallNoticeManager, self).filter(
            reject=False)

    def unvalidated(self):
        return super(SmallNoticeManager, self).filter(
            reject=False, validated=False)

    def validated(self):
        return super(SmallNoticeManager, self).filter(
            reject=False, validated=True)


class SmallNotice(models.Model):

    class Meta:
        verbose_name = _("Small Notice")
        verbose_name_plural = _("Smalls Notices")
        ordering = ['-date']

    name = models.CharField(max_length=200, verbose_name=_("Name"))
    subject = models.CharField(max_length=20, verbose_name=_("Subject"),
                               blank=True)
    body = models.CharField(max_length=200)
    email = models.EmailField(verbose_name=_("Email"), null=True)
    validated = models.BooleanField(verbose_name=_("Validé"), default=False)
    reject = models.BooleanField(verbose_name=_("Réjeter"), default=False)
    date = models.DateTimeField(verbose_name=_("Date"), default=timezone.now)
    count_view = models.IntegerField(default=0)

    objects = SmallNoticeManager()

    def __str__(self):
        return "{sj} / {bdy} / {mbr}".format(
            sj=self.subject, bdy=self.body, mbr=self.name)

    def save(self, *args, **kwargs):

        super(SmallNotice, self).save(*args, **kwargs)


class CommentNotice(models.Model):

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
    date_created = models.DateTimeField(verbose_name=_("Date Created"),
                                        default=timezone.now)
    body = models.CharField(max_length=200, verbose_name=_("Body"))
    small_notice = models.ForeignKey(
        SmallNotice, verbose_name=_("Small notice"))

    def __str__(self):
        return "{}/{}/{}".format(
            self.small_notice, self.date_created, self.body)


class NoticeManager(models.Manager):

    def get_queryset(self):
        return super(NoticeManager, self).get_queryset()

    def notexpired(self):
        return super(NoticeManager, self).filter(
            date_expired__gte=timezone.now())


class Locality(models.Model):

    class Meta:
        verbose_name = _("Locality")
        verbose_name_plural = _("Localities")

    slug = models.SlugField(),
    name = models.CharField(max_length=100, verbose_name=_("Name"))

    def __str__(self):
        return self.name


class CallForTenderManager(models.Manager):

    def get_queryset(self):
        return super(CallForTenderManager, self).get_queryset()

    def notexpired(self):
        return super(CallForTenderManager, self).filter(
            date_expired__gte=timezone.now())


class CallForTender(models.Model):
    """ Offres
    """

    class Meta:
        verbose_name = _("Tender")
        verbose_name_plural = _("Tenders")
        ordering = ['-date_created']

    title = models.CharField(max_length=200, verbose_name=_("Title"))
    locality = models.ForeignKey(Locality, verbose_name=_("Locality"))
    post = models.CharField(max_length=200, verbose_name="")
    body = HTMLField(blank=True, verbose_name=_("Text"))
    count_view = models.IntegerField(default=0, verbose_name=_("Count"))
    share = models.BooleanField(default=True, blank=True)
    organization = models.ForeignKey(
        Organization, verbose_name=_("Organization"))
    slug = models.CharField(
        max_length=200, unique=True, blank=True, verbose_name=_("Slug"))
    date_created = models.DateTimeField(
        verbose_name=_("Dated the"), auto_now=True)
    date_expired = models.DateTimeField(
        verbose_name=_("Date expired"), default=timezone.now)
    lang = models.ForeignKey(
        Language, blank=True, null=True, verbose_name=_("Language"))
    destination_email = models.EmailField(
        verbose_name=_("Email"), unique=True, blank=True)

    objects = CallForTenderManager()

    def __str__(self):
        return "{}/{}/{}".format(self.locality, self.title, self.date_expired)


class Notice(models.Model):
    """ Avis
    """

    class Meta:
        verbose_name = _("Notice")
        verbose_name_plural = _("Notices")
        ordering = ['-date_created']

    locality = models.ForeignKey(Locality, verbose_name=_("Locality"))
    post = models.CharField(max_length=200, verbose_name=_("Poste"))
    contract = models.ForeignKey(Contract, verbose_name=_("Contract"))
    body = HTMLField(blank=True, verbose_name=_("Text"))
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    count_view = models.IntegerField(default=0, verbose_name=_("Count"))
    contract_length = models.IntegerField(
        verbose_name=_("Durée du contrat"), null=True, blank=True)
    share = models.BooleanField(default=True, blank=True)
    organization = models.ForeignKey(
        Organization, verbose_name=_("Organization"))
    slug = models.CharField(
        max_length=200, unique=True, blank=True, verbose_name=_("Slug"))
    date_created = models.DateTimeField(
        verbose_name=_("Dated the"), auto_now=True)
    date_expired = models.DateTimeField(
        verbose_name=_("Date expired"), default=timezone.now)
    lang = models.ForeignKey(
        Language, blank=True, null=True, verbose_name=_("Language"))
    destination_email = models.EmailField(
        verbose_name=_("Email"), unique=True, blank=True)

    objects = NoticeManager()

    @property
    def image(self):
        return None

    def job_active(self):
        return Notice.objects.filter(date_expired__gte=timezone.now)

    def __str__(self):
        return "{}/{} / {}".format(self.contract,
                                   self.title, self.date_expired)

    def is_share(self):
        if not self.share:
            return False
        self.share = False
        return True

    @property
    def get_short_id(self):
        # return short_url.encode_url(self.id)
        return "{}".format(self.id)

    def save(self, *args, **kwargs):
        self.slug = re.sub(
            "[\!\*\’\(\)\;\:\@\&\=\+\$\,\/\?\#\[\](\-)\s \. \؟]+", '-',
            self.title.lower())
        self.share = self.is_share()
        super(Notice, self).save(*args, **kwargs)

    def type_text(self):
        return self.contract

    def post_url(self):
        return os.path.join(
            settings.DOMMAIN, self.lang.slug, "job", self.get_short_id)

    def get_twiter_message(self):
        return u"{} - {}".format(self.type_text(), self.title), self.post_url()
