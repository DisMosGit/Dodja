from django.db import models
from django.conf import settings
from datetime import datetime
from django.utils.translation import gettext_lazy as _
import uuid


class Host(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('title'), max_length=127)
    description = models.TextField(_('description'), default="")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                verbose_name=_('creator'),
                                on_delete=models.CASCADE,
                                related_name='hosts')
    # TODO: Шифрование credentials
    credentials = models.JSONField(_('credentials'))
    settings = models.JSONField(_('settings'))
    date_created = models.DateTimeField(_('date_created'), auto_now_add=True)
    date_updated = models.DateTimeField(_('date_updated'), auto_now=True)

    def __str__(self):
        return self.title

    def set_up_credentials(self):
        return self.credentials


class Access(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.ForeignKey(Host,
                             verbose_name=_('host'),
                             on_delete=models.CASCADE,
                             related_name='accesses')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name=_('user'),
                             on_delete=models.CASCADE,
                             related_name='accesses')
    permissions = models.IntegerField(_('permissions'), default=0)

    permissions_value = {
        0: "",
        1: "r",
        2: "cr",
        3: "cru",
        4: "crud",
        5: "crude",
        6: "re",
        7: "crudeo",
        8: "reo",
        9: "",
    }  # r - read, c - create, u - update, d - delete, e - execute, o - other
    permissions_kind = {
        "dh": 1,  # Host
        "dp": 2,  # DockerPermissions
        "no": 3,  # Note
        "mo": 4,  # Monitoring
        "ml": 5,  # MonitoringLog
        "nf": 6,  # Notification
    }
    permissions_dictionary = {
        "r": "read",
        "c": "create",
        "u": "update",
        "d": "delete",
        "e": "execute",
        "o": "other",
        "dh": "Host",
        "dp": "DockerPermissions",
        "no": "Note",
        "mo": "Monitoring",
        "ml": "MonitoringLog",
        "nf": "Notification",
    }

    def __str__(self):
        return f"{self.user}: {self.host}: {self.permissions}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['host', 'user'],
                                    name='unique_permissions_for_user'),
        ]

    def check_permission(self, kind: str, operation: str) -> bool:
        int_position = self.permissions_kind.get(kind.lower(), 0)
        if int_position:
            permission_value = self.permissions % 10**int_position // 10**(
                int_position - 1)
            if permission_value:
                return operation in self.permissions_value.get(
                    permission_value, "")
            return False
        return True

    def able_operations(self, kind: str) -> list:
        result = []
        int_position = self.permissions_kind.get(kind.lower(), 0)
        if int_position:
            permission_value = self.permissions % 10**int_position // 10**(
                int_position - 1)
            if permission_value:
                result = []
                for operation in self.permissions_value.get(
                        permission_value, ""):
                    result.append(
                        self.permissions_dictionary.get(operation, operation))
        return result


class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.ForeignKey(Host,
                             verbose_name=_('host'),
                             on_delete=models.CASCADE,
                             related_name='jobs')
    task = models.ForeignKey('django_q.task',
                             verbose_name=_('task'),
                             on_delete=models.CASCADE,
                             related_name='host_jobs')
    date_created = models.DateTimeField(_('date_created'), auto_now_add=True)
