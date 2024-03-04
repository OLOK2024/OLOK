from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()
    confirmed_password = serializers.CharField(write_only=True)

    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'date_joined', 'password', 'confirmed_password',
                  'start_of_day', 'end_of_day', 'workdays', 'country_code')

    def validate(self, data):
        if data.get('password') != data.get('confirmed_password'):
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirmed_password')
        user = User.objects.create(email=validated_data['email'],
                                   first_name=validated_data.get('first_name', ''),
                                   last_name=validated_data.get('last_name', ''),
                                   start_of_day=validated_data.get('start_of_day', '00:00'),
                                   end_of_day=validated_data.get('end_of_day', '23:59'),
                                   workdays=validated_data.get('workdays', 0b1111100),
                                   country_code=validated_data.get('country_code', ''))
        user.set_password(validated_data['password'])
        user.save()
        return user
