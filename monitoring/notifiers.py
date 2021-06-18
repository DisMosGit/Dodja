from datetime import datetime
from logging import getLogger

from django.db.models.query_utils import Q
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from utils.renderers import DockerJSONEncoder

from .models import HTMLNotification, NotificationPreferences
from docker_host.models import Host, Access

logger = getLogger(__name__)


class Check():
    pass


class Message():
    def __init__(self, obj_str, checks, launch_time, error) -> None:
        self.checks = checks
        self.launch_time = launch_time
        self.obj_str = obj_str
        self.error = error
        pass

    @property
    def text(self) -> str:
        return f'{self.obj_str} ERROR at {self.launch_time}\n'

    @property
    def json(self) -> str:
        return DockerJSONEncoder().encode(self.dict)

    @property
    def html(self) -> str:
        return f'<h2>{self.obj_str} ERROR at {self.launch_time}</h2>'

    @property
    def dict(self) -> dict:
        return {
            "subject": f'{self.obj_str} ERROR at {self.launch_time}',
            "message": str(self.checks)
        }


class Notifier():
    kind = "none"

    def __init__(self, message) -> None:
        self.message: Message = message

    def send_message(self, user: User, **kwargs):
        raise NotImplementedError()


class EmailNotifier(Notifier):
    kind = "email"

    def send_message(self, user: User, **kwargs):
        pass
        send_mail(
            **self.message.to_dict(),
            settings.EMAIL_HOST,
            (user.email, ),
            fail_silently=False,
        )


class HTMLNotifier(Notifier):
    kind = "html"

    @property
    def _host_id(self):
        return self.message.get("host_id")

    def send_message(self, user: User, **kwargs):
        HTMLNotification(
            user=user,
            host__id=self._host_id,
            message=self.message.json,
            date_expire=kwargs.get("date_expire", None),
        ).save()


class NotifierManager():
    _send_types = {
        0: "",
        1: "email",
        2: "html",
        3: "all",
    }
    notifyer_classes = (Notifier, EmailNotifier, HTMLNotification)

    def __init__(self, **kwargs) -> None:
        self.message = Message(**kwargs)

    def notify(self, host_id: str = None, user_id_list: list = None, **kwargs):
        for preferenses in self.get_user_preferenses_list(
                host_id, user_id_list):
            try:
                kind = self.get_kind(preferenses.user)
                notifier = self.get_notifyer(kind)
                notifier(self.message).send_message(preferenses.user, **kwargs)
            except:
                logger.error('notify error')
        return True

    def get_user_preferenses_list(
        self,
        host_id: str = None,
        user_id_list: list = None,
    ) -> list[Access]:
        if host_id:
            if user_id_list:
                pass
                # Access.objects.filter(host=host, user)
                # TODO: change User to settings.AUTH_USER
                # User.objects.filter(
                # Q(accesses__gte=1) | Q(hosts=host)).all()
            else:
                return Access.objects.filter(
                    Q(host__id=host_id)
                    | Q(user__hosts__id=host_id)).select_related('user').all()
        elif user_id_list:
            pass
        else:
            return []

    def get_kind_by_user(self, user: AbstractUser) -> Notifier:
        if user.last_login > datetime.now() - settings.ACCESS_TOKEN_LIFETIME:
            if user.email:
                return self._send_types.get(3, "")
            else:
                return self._send_types.get(2, "")
        elif user.email:
            return self._send_types.get(1, "")
        return self._send_types.get(0, "")

    def get_kind(self, send_type: int) -> Notifier:
        # TODO: byte calculcations
        return self._send_types.get(send_type, "")

    def get_notifyer(self, kind: str) -> Notifier:
        for notifyer in self.notifyer_classes:
            if notifyer.kind == kind:
                return notifyer