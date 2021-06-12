from rest_framework.utils import encoders
from rest_framework.renderers import JSONRenderer
from docker.models import containers, configs, images, networks, volumes


class DockerJSONEncoder(encoders.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (containers.Container,
                            containers.ContainerCollection, configs.Config)):
            return obj.attrs
        return super().default(obj)


class DockerJSONRenderer(JSONRenderer):
    encoder_class = DockerJSONEncoder