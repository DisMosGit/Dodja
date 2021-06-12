from rest_framework import request
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q

from docker_host.permissions import IsHostOperationAllowed, HostOperationMixin

from .models import Note
from .serializer import NoteSerializer


class NoteView(ModelViewSet, HostOperationMixin):
    queryset = Note.objects
    serializer_class = NoteSerializer
    permission_classes = [IsHostOperationAllowed]
    lookup_field = 'id'
    permission_kind = "no"
    host_pk = "host__pk"

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(host__pk=self.kwargs.get("host__pk")),
            Q(is_public=True) | Q(creator=self.request.user)).order_by('title')

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user,
                        host=self.kwargs.get("host__pk"))
