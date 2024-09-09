from django.db import models
from user.models import User

class Post(models.Model):
    postid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    tags = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    caption = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_posted']
