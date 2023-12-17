from rest_framework import serializers
from .models import Instruments, Order
from rest_framework import serializers
from django.contrib.auth.models import User


class InstrumentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Instruments
        fields = '__all__'


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def validate_email(self, value):
        if not value.endswith('@example.com'):
            raise serializers.ValidationError("Email must end with @example.com")

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email is already in use')
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username is already in use')
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long')
        return value

    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write:only': True}}


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user
