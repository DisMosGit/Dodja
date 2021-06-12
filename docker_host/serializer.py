from rest_framework import serializers
from rest_framework.decorators import permission_classes
from .models import Host, Access, Job
from profile.serializer import UserSerializer


class HostCredentialsSerializer(serializers.Serializer):
    base_url = serializers.CharField(max_length=511)
    version = serializers.CharField(max_length=15, required=False)
    timeout = serializers.IntegerField(required=False)
    tls = serializers.BooleanField(default=False, required=False)
    user_agent = serializers.CharField(max_length=511, required=False)
    credstore_env = serializers.JSONField(required=False)
    use_ssh_client = serializers.BooleanField(default=False, required=False)
    max_pool_size = serializers.IntegerField(required=False)


class HostCredentialsTLSConfigSerializer(serializers.Serializer):
    # client_cert (tuple of str) – Path to client cert, path to client key.
    # ca_cert (str) – Path to CA cert file.
    # verify (bool or str) – This can be False or a path to a CA cert file.
    # ssl_version (int) – A valid SSL version.
    # assert_hostname (bool) – Verify the hostname of the server.
    pass


class HostSettingsSerializer(serializers.Serializer):
    default_permissions = serializers.IntegerField(default=5)
    pass


class HostSerializer(serializers.ModelSerializer):
    credentials = HostCredentialsSerializer()
    settings = HostSettingsSerializer()

    class Meta:
        model = Host
        fields = '__all__'
        read_only_fields = (
            'id',
            'creator',
            'date_joined',
            'date_used',
        )


class AccessReadSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Access
        fields = '__all__'
        read_only_fields = (
            'id',
            'host',
        )


class AccessCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Access
        fields = '__all__'
        read_only_fields = (
            'id',
            'host',
        )


class UserAccessSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    host = serializers.UUIDField()
    permissions = serializers.DictField()

    class Meta:
        read_only_fields = (
            'user',
            'host',
        )


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = (
            'id',
            'date_created',
        )


class HostActionResultSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    args = serializers.JSONField(default={})


class ActionSerializer(serializers.Serializer):
    command = serializers.RegexField(max_length=127,
                                     min_length=3,
                                     regex='[a-zA-Z0-9_.]+',
                                     default="ping")
    args = serializers.JSONField(default={})
