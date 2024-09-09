from django.urls import path
from .views import add_friend,friends_list

urlpatterns = [
    path('add-friend/',add_friend,name='add_fiend'),
    path('friends/',friends_list,name='friends_list'),
]