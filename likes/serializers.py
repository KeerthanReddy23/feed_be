from rest_framework import serializers
from .models import Likes

class Likesserializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = '__all__'