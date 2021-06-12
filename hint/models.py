from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Hint(models.Model):
    key = models.CharField(_('key'), max_length=255)
    title = models.CharField(_('title'), max_length=127, default="Untitled")
    text = models.TextField(_('text'))
    language = models.CharField(_('language'), max_length=7)
    date_created = models.DateTimeField(_('date_created'), auto_now_add=True)
    date_updated = models.DateTimeField(_('date_updated'), auto_now=True)
