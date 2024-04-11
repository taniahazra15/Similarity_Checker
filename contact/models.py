from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import *
from django import forms

# Create your models here.
class Contact(models.Model):
    #user= models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    username=models.CharField(max_length=10)
    email=models.EmailField()
    message=models.CharField(max_length=10,blank=False,null=False)
    def __str__(self):
        return self.username
    