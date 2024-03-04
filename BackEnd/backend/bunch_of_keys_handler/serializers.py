from rest_framework import serializers
from .models import BunchOfKeys, DelBunchOfKeys

class BunchOfKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = BunchOfKeys
        fields = '__all__'

class DelBunchOfKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = DelBunchOfKeys
        fields = '__all__'