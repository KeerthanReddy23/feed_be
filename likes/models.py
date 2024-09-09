from django.db import models
from post.models import Post
from user.models import User

class Likes(models.Model):
    postid = models.ForeignKey(Post,on_delete=models.CASCADE)
    userid = models.ForeignKey(User,on_delete=models.CASCADE)