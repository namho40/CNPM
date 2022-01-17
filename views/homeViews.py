from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from main.models import *

def home(request):
    if not request.user.is_authenticated:
        return redirect('user_login_views')
    blogs = Blog.objects.order_by('?').all()[0:3]
    intro = Blog.objects.order_by('?').all()[0:3]
    videos = VideoPost.objects.order_by('?').all()[0:2]

    params = {'blogs' : blogs, "videos" : videos , "intro" : intro }
       
    return render(request, 'client/views/home.html', params)




