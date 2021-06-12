from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.conf import settings
from django_q.tasks import schedule, Schedule

from .models import Monitoring, MonitoringLog
from .serializer import MonitoringSerializer, MonitoringLogSerializer


class MonitoringView(ModelViewSet):
    queryset = Monitoring.objects.all()
    serializer_class = MonitoringSerializer


class MonitoringLogView(ReadOnlyModelViewSet):
    queryset = MonitoringLog.objects.all()
    serializer_class = MonitoringLogSerializer


# class NotificationPreferences(ReadOnlyModelViewSet):
#     queryset = MonitoringLog.objects.all()
#     serializer_class = MonitoringLogSerializer

# FIXME: no such table: django_q_schedule on first migrate
try:
    if not Schedule.objects.filter(func=settings.MONITORING_LAUNCHER).exists():
        print("Monitroing Task Created")
        schedule(
            settings.MONITORING_LAUNCHER,
            # 3,
            # 4,
            schedule_type="I",
        )
except:
    pass