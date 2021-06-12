from django.contrib import admin
from .models import Monitoring, MonitoringLog, NotificationPreferences, HTMLNotification


@admin.register(Monitoring, MonitoringLog, NotificationPreferences,
                HTMLNotification)
class MonitoringAdmin(admin.ModelAdmin):
    pass