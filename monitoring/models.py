from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid


class Monitoring(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                verbose_name=_('creator'),
                                on_delete=models.CASCADE,
                                related_name="monitoring")
    host = models.ForeignKey('docker_host.Host',
                             verbose_name=_('host'),
                             on_delete=models.CASCADE,
                             related_name='monitroing')
    text = models.TextField(_('text'))
    cron_rule = models.CharField(_('cron_rule'), max_length=255)
    priority = models.BooleanField(_('priority'), default=0)
    condition = models.JSONField(_('condition'))
    is_active = models.BooleanField(_('is_active'), default=False)
    is_lock = models.BooleanField(_('is_lock'), default=False)
    date_created = models.DateTimeField(_('date_created'), auto_now_add=True)
    date_updated = models.DateTimeField(_('date_updated'), auto_now=True)
    last_launch = models.DateTimeField(_('last_launch'), )
    next_launch = models.DateTimeField(_('next_launch'), )


class MonitoringLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    monitoring = models.ForeignKey(Monitoring,
                                   on_delete=models.CASCADE,
                                   related_name="log")
    result = models.JSONField(_('result'))
    is_passed = models.BooleanField(_('is_passed'), default=False)
    is_runtime_error = models.BooleanField(_('is_runtime_error'),
                                           default=False)
    duration = models.DurationField(_('duration'))
    date_created = models.DateTimeField(_('date_created'), auto_now_add=True)


class NotificationPreferences(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=_('user'),
                             on_delete=models.CASCADE,
                             related_name="notification_preferences")
    host = models.ForeignKey('docker_host.Host',
                             verbose_name=_('host'),
                             on_delete=models.CASCADE,
                             related_name='notification_preferences')
    # TODO: BinaryField
    send_type = models.IntegerField(_('send_type'), default=0)


def default_date_expire():
    return timezone.now() + timezone.timedelta(hours=2)


class HTMLNotification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.ForeignKey('docker_host.Host',
                             verbose_name=_('host'),
                             on_delete=models.CASCADE,
                             related_name='html_notifications')
    users = models.JSONField(_('users'))
    message = models.JSONField(_('message'))
    date_expire = models.DateTimeField(_('date_created'),
                                       default=default_date_expire)
    date_created = models.DateTimeField(_('date_created'), auto_now_add=True)
