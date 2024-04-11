from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import *
from django import forms


# Create your models here.
class StudentPannel(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    # assignment_name=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    classcode=models.CharField(max_length=10)
    def __str__(self):
        return self.username

class AssignmentUpload(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100)
    folder_path = models.CharField(max_length=255)
    assignment_name=models.CharField(max_length=100)
    assignment = models.FileField(upload_to="assignments/")
    def __str__(self):
        return self.name

# class Admin(models.Model):
#     user= models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    
class AddCourse(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    classcode=models.CharField(max_length=10)
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    username=models.CharField(max_length=100)
    section = models.CharField(max_length=255, blank=True, null=True)
    room_number = models.CharField(max_length=10)
    subject = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.username

class AddAssignment(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    username=models.CharField(max_length=100)
    folder_path1= models.CharField(max_length=255)
    assignmentName=models.CharField(max_length=100)
    assignment_file=models.CharField(max_length=1000)
    answer=models.FileField(upload_to="Answer/")
    def __str__(self):
        return self.username



    









    
