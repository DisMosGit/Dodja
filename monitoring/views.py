from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.conf import settings
from django_q.tasks import schedule, Schedule

from .models import Monitoring, MonitoringLog
from .serializer import MonitoringSerializer, MonitoringLogSerializer
from .inspectors import single_run_monitroing


class MonitoringView(ModelViewSet):
    queryset = Monitoring.objects.all()
    serializer_class = MonitoringSerializer

    def get_queryset(self):
        return super().get_queryset().filter(
            host__pk=self.kwargs.get("host__pk")).order_by('priority')

    def perform_create(self, serializer):
        serializer.save(host_id=self.kwargs.get("host__pk"),
                        creator=self.request.user)


class MonitoringLogView(ReadOnlyModelViewSet):
    queryset = MonitoringLog.objects.all()
    serializer_class = MonitoringLogSerializer

    def get_queryset(self):
        return super().get_queryset().filter(
            host__pk=self.kwargs.get("host__pk"),
            monitoring__pk=self.kwargs.get("monitoring__pk"),
        ).order_by('date_created')

    def perform_create(self, serializer):
        serializer.save(monitoring_id=self.kwargs.get("monitoring__pk"))


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