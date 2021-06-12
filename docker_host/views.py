from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from django.db.models import Q

from .models import Host, Access, Job
from .serializer import AccessCreateSerializer, AccessReadSerializer, HostSerializer, ActionSerializer, JobSerializer, UserAccessSerializer
from .drivers import DockerConnectionPool
from .permissions import IsHostOperationAllowed, HostOperationMixin


class HostViewSet(ModelViewSet, HostOperationMixin):
    queryset = Host.objects
    serializer_class = HostSerializer
    permission_classes = [IsHostOperationAllowed]
    permission_kind = "dh"
    host_pk = "pk"
    ignored_suffixes = ("List", )

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(creator=self.request.user)
            | Q(accesses__user=self.request.user)).distinct().order_by('title')

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=True,
            methods=['POST'],
            url_path="execute",
            serializer_class=ActionSerializer)
    def execute(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not IsHostOperationAllowed.check_host_permissions(
                request.user,
                IsHostOperationAllowed.get_docker_operation(
                    serializer.data["command"]),
                host__pk=self.kwargs.get(self.host_pk),
                kind=self.permission_kind,
        ):
            raise PermissionDenied()
        instance = self.get_object()
        result = DockerConnectionPool(str(instance.id), instance).execute(
            command=serializer.data.get('command'),
            **serializer.data.get("args"),
        )
        status = 200
        if bool(result.get("error")):
            status = 400
        return Response(result, status=status)

    @action(detail=True,
            methods=['get'],
            url_path="my_access",
            serializer_class=UserAccessSerializer)
    def my_access(self, request, pk, **kwargs):
        permissions = {}
        access: Access = Access.objects.filter(host__pk=pk,
                                               user=request.user).first()
        if access is None:
            permissions = {"full": True}
        else:
            for kind in access.permissions_kind:
                permissions[access.permissions_dictionary.get(
                    kind,
                    kind,
                )] = access.able_operations(kind)
        serializer = self.get_serializer({
            "permissions": permissions,
            "user": request.user.pk,
            "host": pk
        })
        return Response(serializer.data)


class AccessViewSet(ModelViewSet, HostOperationMixin):
    queryset = Access.objects
    serializer_class = AccessReadSerializer
    permission_classes = [IsHostOperationAllowed]
    lookup_field = 'id'
    permission_kind = "dp"
    host_pk = "host__pk"

    def get_serializer_class(self):
        if self.action in ("update", "create", "partial_update"):
            return AccessCreateSerializer
        else:
            return AccessReadSerializer

    def get_queryset(self):
        return super().get_queryset().prefetch_related('user').filter(
            host__pk=self.kwargs.get("host__pk")).order_by('permissions')

    def perform_create(self, serializer):
        serializer.save(host_id=self.kwargs.get("host__pk"))


class JobViewSet(ReadOnlyModelViewSet, HostOperationMixin):
    queryset = Job.objects
    serializer_class = JobSerializer
    permission_classes = [IsHostOperationAllowed]
    lookup_field = 'id'
    permission_kind = "dh"
    host_pk = "host__pk"

    def get_queryset(self):
        return super().get_queryset().filter(
            host__pk=self.kwargs.get("host__pk"))

    # TODO:
    # @action(detail=True,
    #         methods=['GET'],
    #         url_path="job",
    #         serializer_class=ActionSerializer)
    # def job(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     result = DockerConnectionPool(str(instance.id),
    #                                   instance).get_job_result(
    #                                       request.query_params.get("key"))
    #     return Response(result)
