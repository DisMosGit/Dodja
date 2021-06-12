from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
from uuid import uuid4, UUID
from .models import HTMLNotification


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
        if host_id:
            return HTMLNotification.objects.filter(
                host__id=host_id, user=user).all().values(
                    'message', 'date_created').order_by('date_created')
        else:
            return HTMLNotification.objects.filter(user=user).all().values(
                'message', 'date_created').order_by('date_created')

    def process_response(self, request, response: Response):
        if response.status_code:
            host_id = request.headers.get("X-WEBPUSH", None)
            # TODO: remove sended
            if host_id:
                # user = request
                if host_id == "all":
                    response["X-WEBPUSH"] = self._get_notifications_dict(
                        user=request.user, host_id=None)
                elif self._is_validate_uuid(host_id):
                    response["X-WEBPUSH"] = self._get_notifications_dict(
                        user=request.user, host_id=host_id)
                else:
                    response["X-WEBPUSH"] = [{
                        "message": "error",
                        "date_created": None
                    }]
        return response
