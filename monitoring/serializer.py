import re
from rest_framework import serializers
from .models import Monitoring, MonitoringLog
from docker_host.serializer import ActionSerializer


class MonitoringLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLog
        fields = '__all__'
        read_only_fields = ('id', 'monitoring', 'date_created')


class MonitoringConditionExpectedSerializer(serializers.Serializer):
    value = serializers.JSONField()
    parameter = serializers.RegexField(regex=re.compile(r'^[-a-zA-Z0-9_\.]+$'),
                                       max_length=255)
    comparison = serializers.ChoiceField(
        ["eq", "neq", "gt", "gte", "lt", "lte", "in", "nin"])


class MonitoringConditionSerializer(serializers.Serializer):
    action = ActionSerializer()
    expected = MonitoringConditionExpectedSerializer()


class MonitoringSerializer(serializers.ModelSerializer):
    condition = MonitoringConditionSerializer(many=True)

    # statistics = serializers.JSONField(default=dict)

    class Meta:
        model = Monitoring
        fields = '__all__'
        read_only_fields = (
            'id',
            'creator',
            'host',
            'date_created',
            'date_updated',
            'last_launch',
            'next_launch',
        )
