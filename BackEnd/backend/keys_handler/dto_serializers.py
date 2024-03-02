from rest_framework import serializers

class InfoKeySerializer(serializers.Serializer):
    bunchOfKeysId = serializers.CharField(max_length=24)
    keyId = serializers.CharField(max_length=24)

class AddKeySerializer(serializers.Serializer):
    domain = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    bunchOfKeysId = serializers.CharField(max_length=24)

class PutKeyUsernameSerializer(serializers.Serializer):
    bunchOfKeysId = serializers.CharField(max_length=24)
    keyId = serializers.CharField(max_length=24)
    newUsername = serializers.CharField(max_length=255)

class PutKeyPasswordSerializer(serializers.Serializer):
    bunchOfKeysId = serializers.CharField(max_length=24)
    keyId = serializers.CharField(max_length=24)
    newPassword = serializers.CharField(max_length=255)

class PutKeyDomainSerializer(serializers.Serializer):
    bunchOfKeysId = serializers.CharField(max_length=24)
    keyId = serializers.CharField(max_length=24)
    newDomain = serializers.CharField(max_length=255)
