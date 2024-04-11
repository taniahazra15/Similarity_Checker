from django.shortcuts import render, redirect
from django.http import HttpResponse
#for import the model
from .models import*
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# @login_required(login_url="/login_student/")

# @login_required(login_url="/login_admin/")
# Create your views here.
def register_student(request):
    #getting input from frontend
    if request.method == "POST":
        # data=request.POST
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        #for saving the model
        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request,'Username exists')
            return redirect('/register_student/')
        #getting data
        user=User.objects.create(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()
        messages.info(request,'account created successfully')
        return redirect('/register_student/')
    # queryset=Register_student.objects.all()
    # context ={'register_student':queryset}
    return render(request,'signup.html')
    # return render(request,'signup.html')

    
def register_admin(request):
    if request.method == "POST":
        username=request.POST.get('username')

        email=request.POST.get('email')
        password=request.POST.get('password')
        #for saving the model
        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request,'Username exists')
            return redirect('/register_student/')
        #getting data
        user=User.objects.create(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()
        messages.info(request,'account created successfully')
        return redirect('/register_admin/')
        
    return render(request,'signup1.html')
def login_student(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            messages.error(request,'Invalid Username')
            return redirect('/login_student/')
        user = authenticate(username = username, password= password)
        if user is None:
            messages.error(request,'Invalid password')
            return redirect('/login_student/')
        else:
            login(request, user)
            return redirect('/student_home/')
        


    return render(request,'login.html')
def login_admin(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            messages.error(request,'Invalid Admin Name')
            return redirect('/login_admin/')
        user = authenticate(username = username, password= password)
        if user is None:
            messages.error(request,'Invalid password')
            return redirect('/login_admin/')
        else:
            login(request, user)
            return redirect('/service_admin/')
    
    return render(request,'login1.html')

def logout_admin(request):
    logout(request)
    return redirect('/login_admin/')

def logout_user(request):
    logout(request)
    return redirect('/login_student/')