"""
URL configuration for FinalYear project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from home.views import *
from accounts.views import *
from contact.views import *
from service.views import *

urlpatterns = [
    path('',home,name="home"),
    path('register_student/',register_student,name="register1"),
    path('register_admin/',register_admin,name="register2"),
    path('login_admin/',login_admin,name="login1"),
    path('login_student/',login_student,name="login2"),
    path('contact/',contact,name="contact"),
    path('about/',about,name="about"),
    path('service_student/',service_student,name="service1"),
    path('service_admin/',service_admin,name="service2"),
    path('logout_Admin/',logout_admin,name="logout1"),
    path('logout_User/',logout_user,name="logout2"),
    path('add_assignmnet/',add_assignmnet,name="addstudent"),
    path('add_course/',add_course,name="addcourse"),
    path('student_home/',student_home,name="studenthome"),
    path('student_pannel/',student_pannel,name="studentpannel"),
    path('assignmnet_list/',assignmnet_list,name="assignmnetlist"),
    path('Search_classname/',Search_classname,name="SearchClassname"),
    path('Search_answers/',Search_answers,name="SearchAnswers"),
    path('Search_classname_student/',Search_classname_student,name="SearchClassnameStudent"),
    path('check_similarity/',check_similarity,name="CheckSimilarity"),
    path('admin/', admin.site.urls),
    path('media/', include('django.contrib.staticfiles.urls')),  # Serving media files during development
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

