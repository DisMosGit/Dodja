from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import DestroyModelMixin
from django.conf import settings
from django.db.models import Subquery, Count, OuterRef, F, Q
from django_q.tasks import schedule, Schedule

from docker_host.permissions import IsHostOperationAllowed, HostOperationMixin
from .models import Monitoring, MonitoringLog
from .serializer import MonitoringSerializer, MonitoringLogSerializer
from .inspectors import single_run_monitroing


class MonitoringView(ModelViewSet, HostOperationMixin):
    queryset = Monitoring.objects.all()
    serializer_class = MonitoringSerializer
    permission_classes = [IsHostOperationAllowed]
    lookup_field = 'id'
    permission_kind = "mo"
    host_pk = "host__pk"

    def get_queryset(self):
        ## TODO: statistics
        return super().get_queryset().filter(
            host__pk=self.kwargs.get("host__pk")).order_by('priority')

    def perform_create(self, serializer):
        serializer.save(host_id=self.kwargs.get("host__pk"),
                        creator=self.request.user)


class MonitoringLogView(DestroyModelMixin, ReadOnlyModelViewSet,
                        HostOperationMixin):
    queryset = MonitoringLog.objects.all()
    serializer_class = MonitoringLogSerializer
    permission_classes = [IsHostOperationAllowed]
    lookup_field = 'id'
    permission_kind = "ml"
    host_pk = "host__pk"

    def get_queryset(self):
        return super().get_queryset().filter(monitoring__pk=self.kwargs.get(
            "monitoring__pk"), ).order_by('date_created')

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