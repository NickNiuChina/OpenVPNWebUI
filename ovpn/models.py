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
from django.core.validators import MinValueValidator, MaxValueValidator


logger = logging.getLogger(__name__)


class LinkShowType(models.TextChoices):
    I = ('i', _('index'))
    L = ('l', _('list'))
    P = ('p', _('post'))
    A = ('a', _('all'))
    S = ('s', _('slide'))


class Servers(models.Model):
    """OpenVPN servers model"""
    STATUS_CHOICE = [(0, "disabled"), (1, "enabled")]
    STARTUP_CHOICE = [(0, "sysv"), (1, "systemd")]
    LOG_IZE_CHOICE = [(-1, -1), (300, 300), (1000, 1000), (3000, 3000)]

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    server_name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    configuration_dir = models.CharField(max_length=500, null=False, blank=False, unique=True)
    configuration_file = models.CharField(max_length=500, null=False, blank=False)
    status_file = models.CharField(max_length=500, null=True, blank=True)
    log_file_dir = models.CharField(max_length=500, null=True, blank=True)
    log_file = models.CharField(max_length=500, null=True, blank=True)
    startup_type = models.IntegerField(choices=STARTUP_CHOICE, default=1)
    startup_service = models.CharField(max_length=200, null=False, blank=False)
    certs_dir = models.CharField(max_length=200, null=False, blank=False)
    learn_address_script = models.IntegerField(choices=STATUS_CHOICE, default=1)
    managed = models.IntegerField(choices=STATUS_CHOICE, default=1)
    management_port = models.IntegerField(
        null=True,
        blank=True,
        unique=True,
        validators=[MinValueValidator(1025), MaxValueValidator(65536)]
    )
    management_password = models.CharField(max_length=100, null=True, blank=True, default='')
    log_size = models.IntegerField(choices=STARTUP_CHOICE, default=300)
    comment = models.TextField(null=True, blank=True, default='')
    creation_time = models.DateTimeField(default=datetime.datetime.now, null=False, blank=False)
    update_time = models.DateTimeField(auto_now=True, null=False, blank=False)


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
    STATUS_CHOICE = [(0, "offline"), (1, "online")]
    ENABLED_CHOICE = [(0, "disabled"), (1, "enabled")]
    enabled = models.IntegerField(choices=ENABLED_CHOICE, default=1)
    status = models.IntegerField(choices=STATUS_CHOICE, default=1)
    expire_date = models.DateField(default=datetime.datetime(1970, 1, 1))
    create_time = models.DateTimeField(_('creation time'), default=now)
    update_time = models.DateTimeField(_('modify time'), default=now)

