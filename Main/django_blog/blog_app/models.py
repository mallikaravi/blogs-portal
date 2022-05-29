from ast import arg
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from PIL import Image
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
# Create your models here.

STATUS = (

    (0, 'Draft'),

    (1, 'Published')

)

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField( max_length=50)

    last_name = models.CharField( max_length=50)
    
    profile_pic = models.ImageField(upload_to = 'profile_pics', blank = True)

    
    
    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('editprofile', args=(str(self.id)))


class Post(models.Model):
    
    author = models.ForeignKey(User, editable=False, on_delete= models.CASCADE,related_name='blog_posts', null=True)

    title = models.CharField(max_length=200)

    content = models.TextField()

    status = models.IntegerField(choices=STATUS, default=0)

    blog_pic = models.ImageField(upload_to="blog_pics", blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)



    def __str__(self):

        return self.title

    def get_absolute_url(self):
        return reverse('article', args=(str(self.id)))