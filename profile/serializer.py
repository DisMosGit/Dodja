from rest_framework import serializers
from django.contrib.auth import get_user_model


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active',
            'last_login',
            'date_joined',
        )
        read_only_fields = (
            'id',
            'username',
            'is_staff',
            'is_active',
            'last_login',
            'date_joined',
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'date_joined',
        )
        read_only_fields = (
            'id',
            'username',
            'date_joined',
        )
