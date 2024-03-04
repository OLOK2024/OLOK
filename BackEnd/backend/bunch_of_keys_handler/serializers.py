from rest_framework import serializers
from .models import BunchOfKeys, DelBunchOfKeys, PutBunchOfKeys

class BunchOfKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = BunchOfKeys
        fields = '__all__'

class DelBunchOfKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = DelBunchOfKeys
        fields = '__all__'

class PutBunchOfKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = PutBunchOfKeys
        fields = '__all__'