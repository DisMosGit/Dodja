from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Hint
from .serializer import HintSerializer


class HintViewSet(ReadOnlyModelViewSet):
    queryset = Hint.objects
    lookup_field = 'key'
    serializer_class = HintSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().order_by('title')