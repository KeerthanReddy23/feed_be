from django.urls import path
from .views import signup,login,find_user

urlpatterns = [
    path('signup/',signup,name='signup'),
    path('login/',login,name='login'),
    path('users/',find_user,name='find_user'),
]