from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import *
from django import forms
class Login_student(models.Model):
    user= models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=10)
    

class Login_admin(models.Model):
    user= models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=10)

class Register_student(models.Model):
    user= models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    username=models.CharField(max_length=10,blank=False,null=False)
    email=models.EmailField()
    password=models.CharField(max_length=10,blank=False,null=False)
    repeat_password=models.CharField(max_length=10,blank=False,null=False)

class Register_admin(models.Model):
    user= models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    user=models.CharField(max_length=10,blank=False,null=False)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=10)
    repeat_password=models.CharField(max_length=10)
    
