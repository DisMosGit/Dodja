from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.db.models import Q
from .serializer import UserSerializer, ProfileSerializer


class ProfileViewSet(viewsets.GenericViewSet):
    queryset = get_user_model().objects
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset().first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        instance = self.get_queryset().first()
        serializer = self.get_serializer(instance,
                                         data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        host_id = self.request.query_params.get('host_id', None)
        not_host_id = self.request.query_params.get('not_host_id', None)
        if host_id:
            return super().get_queryset().filter(is_active=True).exclude(
                id=self.request.user.id).filter(
                    Q(hosts__id=host_id)
                    | Q(accesses__host__id=host_id)).order_by('username')
        elif not_host_id:
            return super().get_queryset().filter(is_active=True).exclude(
                id=self.request.user.id).exclude(
                    Q(hosts__id=not_host_id)
                    | Q(accesses__host__id=not_host_id)).order_by('username')
        else:
            return super().get_queryset().filter(is_active=True).exclude(
                id=self.request.user.id).order_by('username')