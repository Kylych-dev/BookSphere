from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction

from apps.users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'email': {'required': False},
            'password': {'write_only': True}
        }

    def validate(self, data):
        if User.objects.filter(
                Q(username__iexact=data['username']) |
                Q(email__iexact=data['email'])
        ).exists():
            raise serializers.ValidationError("A user with this email already exists")
        return data

    @transaction.atomic
    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    # tokens = serializers.SerializerMethodField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password")
        return {'user': user}

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_messages = {
        'bad_token': 'Token is invalid or expired',
    }

    def validate(self, data):
        token = data.get('refresh')
        if not token:
            raise serializers.ValidationError(self.default_error_messages['bad_token'])
        return data

    def save(self, **kwargs):
        try:
            RefreshToken(self.validated_data['refresh']).blacklist()
        except TokenError as ex:
            raise serializers.ValidationError("Token is invalid or expired")
