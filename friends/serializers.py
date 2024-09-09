from rest_framework import serializers
from .models import Friends
from user.serializers import UserSerializer

class FriendSerializer(serializers.ModelSerializer):
    friend_info = UserSerializer(source='friend', read_only=True)
    class Meta:
        model = Friends
        fields = ['user', 'friend', 'friend_info']