from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import uuid


class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('title'), max_length=127, default="Untitled")
    text = models.TextField(_('text'))
    host = models.ForeignKey('docker_host.Host',
                             verbose_name=_('host'),
                             on_delete=models.CASCADE,
                             related_name='notes')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                verbose_name=_('creator'),
                                on_delete=models.CASCADE,
                                related_name='notes')
    is_public = models.BooleanField(_('is public'), default=False)
    date_created = models.DateTimeField(_('date_created'), auto_now_add=True)
    date_updated = models.DateTimeField(_('date_updated'), auto_now=True)
