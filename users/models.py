from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password


class User(models.Model):
    LOG_SIZE_CHOICE = [(-1, "All"), (300, 300), (1000, 1000), (3000, 3000)]
    PAGE_SIZE_CHOICE = [(-1, "All"), (50, 50), (100, 100), (200, 200), (500, 500)]
    ENABLED_CHOICE = [(1, "Enabled"), (0, "Disabled")]
    
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    username = models.CharField(max_length=128, unique=True, verbose_name=_('Username'))
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    email = models.EmailField(max_length=128, unique=True, verbose_name=_('Email'))
    group = models.ForeignKey(
        'UserGroup',
        related_name='users',
        on_delete=models.CASCADE,
        blank=False,
        verbose_name=_('User group')
    )
    status = models.IntegerField(choices=ENABLED_CHOICE, default=1, db_comment="User if enabled")
    log_size = models.IntegerField(choices=LOG_SIZE_CHOICE, default=300)
    page_size = models.IntegerField(choices=PAGE_SIZE_CHOICE, default=50)
    
    #: Use this method initial user
    @classmethod
    def initial(cls):
        print("Model initial method executed!")
        super_user = cls.objects.filter(name='super')
        if not super_user:
            user = cls(username='super',
                       password=make_password('super'),
                       name=_('Super'),
                       email='super@example.com',
                       group=UserGroup.initial()
                       )
            user.save()

    def __str__(self):
        return '{0.name}({0.username})'.format(self)


class UserGroup(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=128, verbose_name=_('Name'))

    def __str__(self):
        return self.name

    @classmethod
    def initial(cls):
        super_group = cls.objects.filter(name='SUPER')
        admin_group = cls.objects.filter(name='ADMIN')
        user_group = cls.objects.filter(name='USER')
        guest_group = cls.objects.filter(name='GUEST')
        if not admin_group:
            group = cls(name='ADMIN')
            group.save()
        if not user_group:
            group = cls(name='USER')
            group.save()
        if not guest_group:
            group = cls(name='GUEST')
            group.save()
        if not super_group:
            group = cls(name='SUPER')
            group.save()
        else:
            group = super_group[0]
        return group
