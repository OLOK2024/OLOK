from rest_framework import serializers
from .models import PutProfileData

class PutProfileDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PutProfileData
        fields = '__all__'