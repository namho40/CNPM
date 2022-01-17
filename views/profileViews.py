import email
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from main.models import *


def profile_information_views(request):
    if not request.user.is_authenticated:
        return redirect('user_login_views')
    return render(request, 'client/views/profile_views.html')


def profile_information_post(request):
    if not request.user.is_authenticated:
        return redirect('user_login_views')
    if request.method=='POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        mail = request.POST['mail']
        new_user = User.objects.update(first_name=first_name, email=mail,last_name=last_name)


    messages.success(request, 'Bạn đã cập nhật thông tin thành công')
    return redirect('profile_information_views')

    return


def blogs_list_views():
    return


def blog_update_post():
    return


def video_list_edits(request):

    return render('client/views/video_list_edit')


def video_update_post():
    return


def change_password_views(request):
    return render(request, 'client/views/change_password_views.html')


def change_password_post():
    return
