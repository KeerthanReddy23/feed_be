from django.urls import path
from .views import create_post,all_posts

urlpatterns = [
    path('new-post/',create_post,name='create_post'),
    path('posts/',all_posts,name='all_posts'),
]