from datetime import timedelta, datetime
from logging import getLogger

from django.db.models.query import QuerySet
from django.utils import timezone
from django.conf import settings
from django_q.tasks import async_task
from croniter import croniter

from docker_host.models import Host
from docker_host.drivers import DockerConnectionPool, DockerJob
from monitoring.models import Monitoring, MonitoringLog, NotificationPreferences
from monitoring.notifiers import NotifierManager, Message

logger = getLogger(__name__)


class Compair():
    def compair(self, name: str, **kwargs) -> bool:
        try:
            return getattr(self, f'_{name}')(**kwargs)
        except:
            return None

    def _eq(self, expected_value, obtained_value) -> bool:
        return bool(obtained_value == expected_value)

    def _neq(self, expected_value, obtained_value) -> bool:
        return bool(obtained_value != expected_value)

    def _gt(self, expected_value, obtained_value) -> bool:
        return bool(obtained_value > expected_value)

    def _gte(self, expected_value, obtained_value) -> bool:
        return bool(obtained_value >= expected_value)

    def _lt(self, expected_value, obtained_value) -> bool:
        return bool(obtained_value < expected_value)

    def _lte(self, expected_value, obtained_value) -> bool:
        return bool(obtained_value <= expected_value)

    def _in(self, expected_value, obtained_value) -> bool:
        return bool(obtained_value in expected_value)

    def _nin(self, expected_value, obtained_value) -> bool:
        return bool(obtained_value not in expected_value)


class Checker(Compair):
    split_symbol = "."

    def __init__(self, obtained_result: dict, expected_result: list) -> None:
        self.obtained_result = obtained_result
        self.expected_result = expected_result
        self.result = []
        self.is_passed = True

    def unpack_obtained_value(self, parameter):
        value = None
        value = self.obtained_result
        for attribute in parameter.split(self.split_symbol):
            if isinstance(value, dict):
                value = value.get(attribute)
            elif isinstance(value, (list, str)):
                value = value[int(attribute)]
            else:
                value = None
            if value is None:
                break
        return value

    def check_condition(self, expected_result):
        for expected in expected_result:
            check = False
            error = ""
            obtained_value = None
            try:
                obtained_value = self.unpack_obtained_value(
                    expected["parameter"])
                check = self.compair(
                    name=expected["comparison"],
                    expected_value=expected["value"],
                    obtained_value=obtained_value,
                )
                if not check:
                    self.is_passed = False
                    error = "Failure"
            except Exception as e:
                check = False
                self.is_passed = False
                error = str(e)
            finally:
                yield {
                    "check": check,
                    "obtained_value": obtained_value,
                    "expected_value": expected["value"],
                    "parameter": expected["parameter"],
                    "comparison": expected["comparison"],
                    "error": error if error else "",
                }

    def check(self):
        try:
            if isinstance(self.expected_result, dict):
                _expected_result = []
                _expected_result.append(self.expected_result.copy())
                for result in self.check_condition(_expected_result):
                    self.result.append(result)
            elif isinstance(self.expected_result, list):
                for result in self.check_condition(
                        self.expected_result.copy()):
                    self.result.append(result)
            else:
                raise Exception("Сondition not specified")
        except Exception as e:
            self.result.append({"check": False, "error": str(e)})
            self.is_passed = False
        finally:
            return self.result, self.is_passed


class Inspector():
    check_class = Checker

    def __init__(self, launch_time: datetime, monitoring: Monitoring) -> None:
        self.launch_time = launch_time if launch_time else timezone.now()
        self._end_time = None
        self.monitoring = monitoring
        self.log = None
        self.lock_task()
        self.error = False
        self.is_passed = False

    def __del__(self):
        self.unlock_task()

    @property
    def end_time(self):
        return self._end_time if self._end_time else timezone.now()

    @end_time.setter
    def end_time(self, value: datetime):
        self._end_time = value

    @property
    def condition(self):
        return self.monitoring.condition

    @property
    def duration(self):
        return self.end_time - self.launch_time

    def start(self, save_log: bool = True, notify: bool = False):
        try:
            job: DockerJob = DockerConnectionPool(
                host_id=self.monitoring.host_id).execute(
                    command=self.condition["action"]["command"],
                    is_background=False,
                    **self.condition["action"]["args"],
                )
            self.end_time = timezone.now()
            self.error = job["error"] if job["error"] else ""
        except Exception as e:
            self.error = str(e)
        checks = []
        if self.error:
            self.save_log(
                is_passed=False,
                is_runtime_error=True,
                result={"error": job["error"]},
            )
        else:
            checks, self.is_passed = self.check_execute_result(
                job["data"], self.condition["expected"])
            self.save_log(
                is_passed=self.is_passed,
                is_runtime_error=False,
                result=checks,
            )
        if notify and not self.is_passed:
            NotifierManager(
                obj_str=str(self.monitoring.text),
                checks=checks,
                launch_time=self.launch_time,
                error=self.error,
            ).notify(host_id=self.monitoring.host_id)
        return self.is_passed, self.error, self.log

    def check_execute_result(self, obtained_result: dict,
                             expected_result: list[dict]):
        return self.check_class(obtained_result, expected_result).check()

    def unlock_task(self) -> Monitoring:
        self.monitoring.is_lock = False
        self.monitoring.next_launch = self._calculate_next_launch(
            self.monitoring.cron_rule, self.end_time)
        self.monitoring.save(update_fields=("next_launch", "is_lock"))

    def lock_task(self) -> Monitoring:
        self.monitoring.is_lock = True
        self.monitoring.last_launch = self.launch_time
        self.monitoring.save(update_fields=("last_launch", "is_lock"))

    def save_log(self, is_passed: bool, is_runtime_error: bool,
                 result: dict) -> MonitoringLog:
        self.log = MonitoringLog(
            monitoring=self.monitoring,
            result=result,
            is_passed=is_passed,
            is_runtime_error=is_runtime_error,
            duration=self.duration,
        )
        self.log.save()

    def _calculate_next_launch(self, cron_rule: str, current_time):
        if cron_rule.isdigit():
            return timedelta(seconds=int(cron_rule)) + current_time
        return croniter(cron_rule, current_time).get_next(datetime)


def create_and_start_inspector(launch_time,
                               monitoring,
                               save_log=True,
                               notify=False):
    inspector = Inspector(launch_time, monitoring)
    return inspector.start(save_log, notify)


class InspectorPool():
    users: list = []

    def start(self):
        result = {}
        launch_time = timezone.now()
        for host in self.get_host_list():
            result[host.pk] = []
            for monitoring in self.get_monitoring_list(host):
                task_id = async_task(create_and_start_inspector,
                                     launch_time=launch_time,
                                     monitoring=monitoring,
                                     save_log=True,
                                     notify=True)
                result[host.pk].append((monitoring.id, task_id))
        return result

    @classmethod
    def get_host_list(cls) -> QuerySet[Host]:
        return Host.objects.filter().all()

    @classmethod
    def get_monitoring_list(cls, host) -> QuerySet[Monitoring]:
        current_time = timezone.now()
        return Monitoring.objects.filter(
            host=host,
            is_active=True,
            is_lock=False,
            next_launch__lte=current_time,
        ).all().order_by("priority")


def single_run_monitroing():
    try:
        return InspectorPool().start()
    except Exception as e:
        logger.error(e)
        raise e
