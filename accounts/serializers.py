from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class AuthUserSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True,
                                                  style={'input_type': 'password', 'placeholder': 'Password'})
    password = serializers.CharField(write_only=True,
                                     style={'input_type': 'password', 'placeholder': 'Password'})

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password_confirmation']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirmation'):
            raise ValidationError("Passwords don't match")

        return attrs


class DummySerializer(serializers.Serializer):
    pass
