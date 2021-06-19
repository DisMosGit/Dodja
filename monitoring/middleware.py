from uuid import uuid4, UUID
from django.db.models.query import QuerySet

from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response

from .models import HTMLNotification
from utils.renderers import DockerJSONEncoder


class HTMLNotifierMiddleware(MiddlewareMixin):
    def process_request(self, request):
        return None

    @staticmethod
    def _is_validate_uuid(s) -> bool:
        try:
            return bool(UUID(str(s)))
        except ValueError:
            return False

    @staticmethod
    def _get_notifications_dict(
        user,
        host_id: str,
    ) -> list[dict]:
        notifications = HTMLNotification.objects.filter(users=user).all()
        result = DockerJSONEncoder().encode(
            notifications.values('message',
                                 'date_created').order_by('-date_created'))
        for n in notifications:
            if len(n.users.all()) >= 2:
                n.users.remove(user)
            else:
                n.delete()
        return result

    def process_response(self, request, response: Response):
        if response.status_code:
            host_id = request.headers.get("X-WEBPUSH", None)
            if host_id:
                notifications = self._get_notifications_dict(user=request.user,
                                                             host_id=None)
                response["X-WEBPUSH"] = notifications
        return response
