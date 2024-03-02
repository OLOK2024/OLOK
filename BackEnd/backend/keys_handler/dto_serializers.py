from rest_framework import serializers

class DelKeySerializer(serializers.Serializer):
    bunchOfKeysId = serializers.CharField(max_length=24)
    keyId = serializers.CharField(max_length=24)

class AddKeySerializer(serializers.Serializer):
    domain = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    bunchOfKeysId = serializers.CharField(max_length=24)