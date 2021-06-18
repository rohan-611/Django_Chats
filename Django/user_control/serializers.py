from rest_framework import serializers
from .models import UserProfile, CustomUser


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class CustomUserSeriealizer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ("password",)


class UserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSeriealizer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserProfile
        fields = "__all__"
