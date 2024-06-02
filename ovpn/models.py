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
from django.core.validators import int_list_validator, validate_comma_separated_integer_list


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

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    server_name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    configuration_dir = models.CharField(max_length=200, null=False, blank=False, unique=True)
    configuration_file = models.CharField(max_length=200, null=False, blank=False)
    status_file = models.CharField(max_length=200, null=True, blank=True)
    log_file_dir = models.CharField(max_length=200, null=True, blank=True)
    log_file = models.CharField(max_length=200, null=True, blank=True)
    startup_type = models.IntegerField(choices=STARTUP_CHOICE, default=1, db_comment="1: systemd, 0: sysv")
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
    comment = models.TextField(null=True, blank=True, default='')
    creation_time = models.DateTimeField(default=datetime.datetime.now, null=False, blank=False)
    update_time = models.DateTimeField(auto_now=True, null=False, blank=False)


class ClientList(models.Model):
    """OpenVPN client model"""
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

class ClientListConfig(models.Model):
    """OpenVPN client proxy config model"""
    validate_comma_separated_integer_list = int_list_validator(
        message=_("Enter only digits separated by commas."),
    )
    OS_TYPE_CHOICE = [(0, "Linux"), (1, "Windows"), (2, "MacOS"), (3, "Others")]
    PROXY_CHOICE = [(0, "disabled"), (1, "enabled")]
    
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    ovpn_client = models.ForeignKey(
        ClientList,
        verbose_name=_('ovpn_client'),
        blank=False,
        null=False,
        on_delete=models.CASCADE)
    os_type = models.IntegerField(choices=OS_TYPE_CHOICE, default=0, null=True, blank=True)
    http_proxy = models.IntegerField(choices=PROXY_CHOICE, default=0, null=True, blank=True)
    https_proxy = models.IntegerField(choices=PROXY_CHOICE, default=0, null=True, blank=True)
    http_port = models.CharField(validators=[validate_comma_separated_integer_list], max_length=200, null=True, blank=True)
    https_port = models.CharField(validators=[validate_comma_separated_integer_list], max_length=200, null=True, blank=True)
    http_proxy_template = models.TextField(max_length=2000, null=True, blank=True)
    ssh_proxy = models.IntegerField(choices=PROXY_CHOICE, default=0)
    ssh_proxy_port = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(22), MaxValueValidator(65536)]
    )
    create_time = models.DateTimeField(_('creation time'), default=now)
    update_time = models.DateTimeField(_('modify time'), default=now)