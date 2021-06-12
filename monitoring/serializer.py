from rest_framework import serializers
from .models import Monitoring, MonitoringLog
from docker_host.serializer import ActionSerializer


class MonitoringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitoring
        fields = '__all__'
        read_only_fields = ('id', )


class MonitoringLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringLog
        fields = '__all__'
        read_only_fields = ('id', )


class MonitoringConditionExpectedSerializer(serializers.Serializer):
    value = serializers.Field()
    parameter = serializers.SlugField(max_length=255)
    comparison = serializers.ChoiceField(
        ["eq", "neq", "gt", "gte", "lt", "lte", "in", "nin"])


class MonitoringConditionSerializer(serializers.Serializer):
    action = ActionSerializer()
    expected = MonitoringConditionExpectedSerializer(many=True)
