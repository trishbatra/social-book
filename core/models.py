from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import  datetime
User = get_user_model()
# Create your models here.
class profile(models.Model):
    user  =  models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileImg = models.ImageField(upload_to="profile_imgs", default="blank.jpeg")
    location = models.CharField( max_length=150, blank=True)

    def __str__(self):
        return self.user.username
class followersCount(models.Model):
    user = models.CharField(max_length=500)
    gotFollowedBy = models.CharField(max_length=500)
    def __str__(self):
        return self.user
class post(models.Model):
    id   =  models.UUIDField(primary_key=True, default=uuid.uuid4)
    user  =  models.CharField(max_length=50)
    image   = models.ImageField (upload_to="myPosts")
    caption   = models.TextField()
    createdAt   = models.DateTimeField(default=datetime.now)
    noOfLikes =   models.IntegerField(default=0)

    def __str__(self) :
        return self.user

class likedpost(models.Model):
    postID  = models.CharField( max_length=50)
    likedBy =  models.CharField( max_length=50)

    def __str__(self) :
        return self.likedBy

