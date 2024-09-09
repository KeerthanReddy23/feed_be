from django.urls import path
from .views import like, post_likes

urlpatterns = [
    path('like/',like,name='like'),
    path('likes/<int:postid>',post_likes,name='post_likes'),
]