from rest_framework import serializers
from .models import BunchOfKeys

class BunchOfKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = BunchOfKeys
        fields = '__all__'