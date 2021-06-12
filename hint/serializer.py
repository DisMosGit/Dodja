from rest_framework.serializers import ModelSerializer
from .models import Hint


class HintSerializer(ModelSerializer):
    class Meta:
        model = Hint
        fields = '__all__'
        read_only_fields = ('id', )
