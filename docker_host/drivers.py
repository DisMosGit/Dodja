from typing import Any, Callable, List, Union
from docker import DockerClient
from datetime import datetime
from time import sleep
from io import BytesIO

from django_q.tasks import async_task, async_iter, result

from docker_host.models import Host, Job

try:
    from django.utils.translation import gettext_lazy as _
except ImportError:

    def _(s):
        return s


class DockerJob():
    def __init__(self, command: str, connection_key: str) -> None:
        self.error = None
        self.data: dict = {}
        self.command: str = command
        self.stop = False
        self.connection_key: str = connection_key

    def __iter__(self):
        yield "error", self.error
        yield "data", self.data
        yield "command", self.command
        yield "stop", self.stop
        yield "connection_key", self.connection_key
        yield "job_id", None

    def do(self, func: Callable, is_iterable: bool = False, **kwargs) -> dict:
        try:
            if is_iterable:
                self.data = {}
                for number, row in enumerate(func(**kwargs)):
                    if self.stop:
                        break
                    self.data[number] = row
            else:
                _data = func(**kwargs)
                if isinstance(_data, (int, str, float, bool, type(None))):
                    _data = {"state": _data}
                self.data = _data
            self.stop = True
        except Exception as e:
            self.set_error(str(e))
        finally:
            return self.data

    def get_function(self, obj, command: str) -> Callable:
        if not command:
            return None
        for attribute in command.split("."):
            obj = getattr(obj, attribute, None)
        # if isinstance(obj, Callable):
        return obj

    def start(self, is_iterable: bool, **kwargs) -> dict:
        func = self.get_function(
            DockerConnectionPool(
                self.connection_key).get_connection().connection, self.command)
        if not func:
            self.set_error("no function")
            raise Exception("no function")
        self.do(func, is_iterable, **kwargs)
        return dict(self)

    def set_error(self, e: str) -> None:
        self.error = _(str(e))


class DockerConnection():
    def __init__(self, docker_host: Host) -> None:
        self.make_settings(docker_host)
        self.make_connection(docker_host)
        self.id = docker_host.id
        self.error: Exception = None

    def __del__(self):
        try:
            self.connection.close()
        except:
            pass

    def make_settings(self, docker_host) -> None:
        self.settings = docker_host.settings.copy()

    def make_connection(self, docker_host) -> None:
        try:
            self.connection = DockerClient(**docker_host.set_up_credentials())
        except Exception as e:
            self.error = e
            raise Exception()

    def healt_check(self) -> bool:
        try:
            return self.connection.ping()
        except Exception as e:
            self.error = e
            return False


class DockerConnectionPool():
    connections: dict[str, DockerConnection] = {}

    def __init__(
        self,
        host_id: str,
        docker_host: Host = None,
    ) -> DockerConnection:
        self.host_id = host_id
        self.connection: DockerConnection = None
        self.get_connection(docker_host)

    def get_connection(self, docker_host: Host = None) -> DockerConnection:
        self.connection = self.connections.get(self.host_id, None)
        if self.connection is None:
            if not self.host_id is None:
                return self.create_connection(
                    Host.objects.get(id=self.host_id))
            else:
                return self.create_connection(docker_host)
        else:
            if self.connection.healt_check():
                return self.connections[self.host_id]
            else:
                self.kill_connection()
                return self.create_connection(docker_host)

    def create_connection(self, docker_host: Host) -> DockerConnection:
        docker_connection = DockerConnection(docker_host)
        self.connections[self.host_id] = docker_connection
        self.connection = docker_connection
        return self.connection

    def kill_connection(self) -> bool:
        del self.connection
        self.connection = None
        return bool(self.connections.pop(self.host_id, None))

    def get_job_result(self, job_key) -> Any:
        if Job.objects.filter(host__id=self.host_id,
                              task__id=job_key).exists():
            return result(job_key)

    def kwargs_filter(self, command: str, kwargs):
        if command == "api.build":
            if isinstance(kwargs.get("fileobj", None), str):
                kwargs["fileobj"] = BytesIO(kwargs["fileobj"].encode('utf-8'))
        elif command == "api.build":
            pass
        return kwargs

    def execute(self,
                command: str,
                is_background: bool = False,
                is_iterable: bool = False,
                **kwargs) -> dict:
        print(kwargs)
        kwargs = self.kwargs_filter(command, kwargs)
        if is_background:
            return {
                "job_id":
                self._background_execute(
                    command,
                    is_iterable,
                    **kwargs,
                )
            }
        else:
            return self._live_execute(
                command,
                is_iterable,
                **kwargs,
            )

    def _background_execute(self,
                            command: str,
                            is_iterable: bool = False,
                            **kwargs) -> Union[None, dict]:
        job = DockerJob(command, self.host_id)
        # TODO: real time updating
        # TODO: using same DockerConnections
        job_id = async_task(job.start, is_iterable, **kwargs)
        # FIXME: FOREIGN KEY constraint failed
        sleep(2)
        Job(host_id=self.host_id, task_id=job_id).save()
        return job_id

    def _live_execute(self,
                      command: str,
                      is_iterable: bool = False,
                      **kwargs) -> Union[None, dict]:
        job = DockerJob(command, self.host_id)
        return job.start(is_iterable, **kwargs)
