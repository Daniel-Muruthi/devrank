from django.db import models
import datetime as dt
from datetime import datetime 
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.shortcuts import get_object_or_404,render,HttpResponseRedirect
from cloudinary.models import CloudinaryField
from tinymce.models import HTMLField
from django.contrib import auth
from django.utils.text import slugify 
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver


class Subscriber(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    def __str__(self):
        return self.name
class Location(models.Model):
    location=models.CharField(max_length=30)

    objects = models.Manager()

    def __str__(self):
        return self.location


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,)
    comment = models.TextField(null=True)
    date = models.DateField(auto_now_add=True, null=True)
    project = models.ForeignKey('Project', related_name="comments", on_delete=models.CASCADE, null=True,)


    objects = models.Manager()

    def __str__(self):
        return self.user.username
    def get_absolute_url(self):
        return reverse('addcomment', kwargs={'pk': self.pk})

    @classmethod
    def show_projects(cls):
        comments = cls.objects.all()
        return comments
    def savecomment(self):
        self.save()

GENDER_CHOICES = (
   ('M', 'Male'),
   ('F', 'Female'),
   ('O', 'Other')
)


class UserProfile(models.Model):
    title= models.CharField(null=True, max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    email = models.CharField(null=True, max_length=255)
    phonenumber = models.IntegerField(null=True)
    bio = models.CharField(blank=True,max_length=255)
    userpic = CloudinaryField('image')
    gender = models.CharField(max_length=11, choices=GENDER_CHOICES, default='Male')

    def __str__(self):
        return self.user.username

    @classmethod
    def getProfileByName(cls, username):
        uprofile = cls.objects.filter(username=username)
        return uprofile


class Project(models.Model):
    title = models.CharField(null=True, max_length=255)
    name = models.CharField(null=True, max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    userpic = CloudinaryField('image')
    description = models.CharField(blank=True,max_length=255)
    livelink = models.URLField()
    pub_date = models.DateTimeField(auto_now_add=True, null=True)
    likes = models.IntegerField(default=0)


    # objects = models.Manager()

    def get_absolute_url(self):
        return reverse('findpost', kwargs={'pk': self.pk})

    @classmethod
    def show_projects(cls):
        projects = cls.objects.all()
        return projects


    @classmethod
    def getprojectbyid(cls, id):
        projects = cls.objects.filter(id=id)
        return projects

    @classmethod
    def getprojectbytitle(cls, searchtitle):
        getproject = cls.objects.filter(title=searchtitle)
        return getproject

class ProjectRating(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    project = models.OneToOneField(Project, on_delete=models.CASCADE, null=True)
    rating = models.IntegerField()
