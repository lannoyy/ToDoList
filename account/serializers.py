from rest_framework import serializers


class SignInSerializer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField()
    organisation = serializers.CharField()
