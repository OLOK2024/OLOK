from rest_framework import serializers
from .models import Key, InfoKey, AddKey, PutKeyUsername, PutKeyPassword, PutKeyDomain

class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = '__all__'

class InfoKeySerializer(serializers.Serializer):
    class Meta:
        model = InfoKey
        fields = '__all__'

class AddKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = AddKey
        fields = '__all__'

class PutKeyUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PutKeyUsername
        fields = '__all__'

class PutKeyPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PutKeyPassword
        fields = '__all__'

class PutKeyDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = PutKeyDomain
        fields = '__all__'