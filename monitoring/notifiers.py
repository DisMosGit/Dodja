from datetime import timedelta
from django.utils import timezone
from logging import getLogger

from django.db.models.query_utils import Q
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
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
    def subject(self) -> str:
        return f'Dodja {self.obj_str} ERROR'

    @property
    def message(self) -> str:
        msg = f'{self.launch_time}\n{self.error}' if self.error else f'{self.launch_time}'
        if isinstance(self.checks, list):
            for check in self.checks:
                msg += f'\n{"✓" if check.get("check") else "✕"}|'
                msg += f'{check.get("parameter", "")}→{check.get("obtained_value", "")}~{check.get("error", "")}'
        return msg


class Notifier():
    kind = "none"

    def __init__(self, message) -> None:
        self.message: Message = message

    def send_message(self, user: AbstractUser, **kwargs):
        pass


class EmailNotifier(Notifier):
    kind = "email"

    def send_message(self, user: AbstractUser, **kwargs):
        send_mail(self.message.subject, self.message.message,
                  settings.EMAIL_HOST_USER, (user.email, ))


class HTMLNotifier(Notifier):
    kind = "html"

    def send_message(self, user: AbstractUser, **kwargs):
        n = HTMLNotification(
            subject=self.message.subject,
            message=self.message.message,
            date_expire=kwargs.get("date_expire",
                                   timezone.now() - timedelta(days=1)),
        )
        n.save()
        n.users.add(user)


class AllNotifier(Notifier):
    kind = "all"
    notifyer_classes = (EmailNotifier, HTMLNotifier)

    def send_message(self, user: AbstractUser, **kwargs):
        for notifier in self.notifyer_classes:
            notifier(self.message).send_message(user, **kwargs)


class NotifierManager():
    _send_types = {
        0: "",
        1: "email",
        2: "html",
        3: "all",
    }

    notifyer_classes = (Notifier, EmailNotifier, HTMLNotifier, AllNotifier)

    def __init__(self, **kwargs) -> None:
        self.message = Message(**kwargs)

    def notify(self, host_id: str = None, user_id_list: list = None, **kwargs):
        for preferenses in self.get_user_preferenses_list(
                host_id, user_id_list):
            try:
                notifier = self.get_notifyer(
                    self.get_kind_by_user(preferenses))
                notifier(self.message).send_message(preferenses, **kwargs)
            except Exception as e:
                logger.error(f'notify error {str(e)}')
        return True

    def get_user_preferenses_list(
        self,
        host_id: str = None,
        user_id_list: list = None,
    ) -> list[AbstractUser]:

        if host_id:
            if user_id_list:
                pass
                # Access.objects.filter(host=host, user)
                # TODO: change User to settings.AUTH_USER
                # User.objects.filter(
                # Q(accesses__gte=1) | Q(hosts=host)).all()
            else:
                return get_user_model().objects.filter(
                    Q(accesses__host__id=host_id)
                    | Q(hosts__id=host_id)).all()
        elif user_id_list:
            pass
        else:
            return []

    def get_kind_by_user(self, user: AbstractUser) -> Notifier:
        if user.last_login > timezone.now(
        ) - settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]:
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