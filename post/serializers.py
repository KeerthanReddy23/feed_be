from rest_framework import serializers
from .models import Post
from likes.models import Likes

class Postserializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField()
    liked_users = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['postid', 'userid', 'image', 'tags', 'place', 'caption', 'date_posted', 'total_likes', 'liked_users']

    def get_total_likes(self, obj):
        return Likes.objects.filter(postid=obj.postid).count()
    
    def get_liked_users(self, obj):
        users = Likes.objects.filter(postid=obj.postid)
        liked_users = [user.userid.pk for user in users]
        return liked_users