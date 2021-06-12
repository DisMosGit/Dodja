from rest_framework import permissions

from .models import Access
from .models import Host


class HostOperationMixin():
    permission_kind: str = None
    host_pk: str = "pk"
    ignored_suffixes: tuple = ()
    action_to_operation: dict = {
        "create": "c",
        "list": "r",
        "retrieve": "r",
        "update": "u",
        "partial_update": "u",
        "destroy": "d",
        "execute": "e",
        "default": "r",
    }

    def _get_operation(self) -> str:
        return self.action_to_operation.get(
            self.action, self.action_to_operation.get("default"))


class IsHostOperationAllowed(permissions.IsAuthenticated):
    docker_action_to_operation: dict[str, list] = {
        "r": (
            "containers.get",
            "containers.list",
            "container.logs",
            "api.ping",
            "ping",
            "api.containers",
            "api.inspect_container",
            "api.images",
            "api.inspect_image",
            "api.networks",
            "api.inspect_network",
            "api.volumes",
            "api.inspect_volume",
            "api.info",
            "api.version",
        ),
        "default":
        "e",
    }

    def has_permission(self, request, view: HostOperationMixin):
        if not super().has_permission(request, view):
            return False
        else:
            if view.permission_kind and view.suffix not in view.ignored_suffixes:
                return self.check_host_permissions(
                    operation=view._get_operation(),
                    user=request.user,
                    host__pk=view.kwargs.get(view.host_pk),
                    kind=view.permission_kind,
                )
            else:
                return True

    @classmethod
    def check_host_permissions(cls,
                               user,
                               operation: str,
                               host__pk=None,
                               kind=None) -> bool:
        if Host.objects.filter(pk=host__pk, creator=user).exists():
            return True
        else:
            perm: Access = Access.objects.filter(host__pk=host__pk,
                                                 user=user).first()
            if perm is None:
                return False
            else:
                return perm.check_permission(
                    kind=kind,
                    operation=operation,
                )

    @classmethod
    def get_docker_operation(cls, command: str) -> str:
        for operation in cls.docker_action_to_operation:
            if command in cls.docker_action_to_operation[operation]:
                return operation
        return cls.docker_action_to_operation["default"]