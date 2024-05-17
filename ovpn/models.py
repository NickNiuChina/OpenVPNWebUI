import logging
from abc import abstractmethod

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
import datetime
import uuid


logger = logging.getLogger(__name__)


class LinkShowType(models.TextChoices):
    I = ('i', _('index'))
    L = ('l', _('list'))
    P = ('p', _('post'))
    A = ('a', _('all'))
    S = ('s', _('slide'))


class Servers(models.Model):
    """OpenVPN servers model"""
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    server_name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    configuration_dir = models.CharField(max_length=500, null=False, blank=False)
    service_cmd = models.CharField(max_length=200, null=False, blank=False)
    STATUS_CHOICE = [(0, "disabled"), (1, "enabled")]
    learn_address_script = models.IntegerField(choices=STATUS_CHOICE, default=1)
    managed = models.IntegerField(choices=STATUS_CHOICE, default=1)
    comment = models.TextField(null=True, blank=True, default='')
    creation_time = models.DateTimeField(default=datetime.datetime.now, null=False, blank=False)
    update_time = models.DateTimeField(default=datetime.datetime.now, null=False, blank=False)


class ClientList(models.Model):
    """OpenVPN servers model"""
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    server = models.ForeignKey(
        Servers,
        verbose_name=_('server'),
        blank=False,
        null=False,
        on_delete=models.CASCADE)
    site_name = models.CharField(max_length=100, null=True, blank=True)
    cn = models.CharField(max_length=100, null=False, blank=False, unique=True)
    ip = models.CharField(max_length=20, null=False, blank=False, unique=True)
    toggle_time = models.DateTimeField(default=now)
    STATUS_CHOICE = {0, 1}
    enabled = STATUS_CHOICE
    expire_date = models.DateField(default=now)
    creation_time = models.DateTimeField(_('creation time'), default=now)
    last_modify_time = models.DateTimeField(_('modify time'), default=now)

