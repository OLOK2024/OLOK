from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()
    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'date_joined', 'password', 'start_of_day', 
                  'end_of_day', 'workdays')

    def create(self, validated_data):
        user = User.objects.create(email=validated_data['email'],
                                   first_name=validated_data.get('first_name', ''),
                                   last_name=validated_data.get('last_name', ''),
                                   start_of_day=validated_data.get('start_of_day', '00:00'),
                                   end_of_day=validated_data.get('end_of_day', '23:59'),
                                   workdays=validated_data.get('workdays', 0b1111100))
        user.set_password(validated_data['password'])
        user.save()
        return user