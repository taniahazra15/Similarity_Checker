from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import*
from django.contrib.auth.models import User
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views.generic.detail import DetailView
from difflib import SequenceMatcher
import aspose.words as aw
import fitz 
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import send_mail, BadHeaderError
def contact(request):
    if request.method == "POST":
        username=request.POST.get('username')
        email=request.POST.get('email')
        message=request.POST.get('message')
        
        #getting data
        user=Contact.objects.create(
            username=username,
            email=email,
            message=message,
            # user=request.user
        )
        messages.info(request,'Message Send successfully')
        try:
            send_mail(username, message, email, ["hazratania16@gmail.com"])
        except BadHeaderError:
            return HttpResponse("Invalid header found.")
        return redirect("/contact/")
        
    

    return render(request,"contact_us.html")
def about(request):
    return render(request,"about.html")
# Create your views here.
