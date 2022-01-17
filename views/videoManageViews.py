
import math
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from main.models import *


def pagination_result(page, item_per_page, total_page):
    page -= 1
    page = 0 if page < 0 else page
    page = total_page if page > total_page else page

    start = page*item_per_page
    end = item_per_page * page + item_per_page
    return page, start, end


def video_list_manage_views(request, page=1):
    item_per_page = 3
    total_item = VideoPost.objects.count()
    total_page = math.floor(total_item / item_per_page)
    pagination = pagination_result(page, item_per_page, total_page)

    video_post = VideoPost.objects.order_by(
        '-id').all()[pagination[1]: pagination[2]]

    for item in video_post:
        item.pub_date = item.pub_date.strftime("%d/%m/%Y")
    params = {
        'video': video_post,
        'total': range(1, total_page + 1),
        'page': page}
    return render(request, 'client/views/video_manage_views.html', params)


def video_edit_views(request, id):
    if not request.user.is_authenticated:
        return redirect('user_login_views')
    video = VideoPost.objects.filter(id=id).first()
    params = {'video': video, 'id' : id}
    return render(request, 'client/views/video_edit_views.html', params)


def video_update_post(request, id):
    if request.method != 'POST':
        return redirect('user_login_views')
    if not request.user.is_authenticated:
        return redirect('user_login_views')
    video = VideoPost.objects.filter(id=id).first()
    title = request.POST['title']
    if(title != ""):
        video.title = title
    desc = request.POST['desc']
    if(desc != ""):
        video.desc = desc
    video_file = request.FILES['fileName'] if 'fileName' in request.FILES else False
    if(video_file != False):
        video.video_file = video_file
    thumb_nail = request.FILES['thumbnail_img'] if 'thumbnail_img' in request.FILES else False
    if(thumb_nail != False):
        video.thumbnail = thumb_nail
    cate = request.POST['category']
    if(cate != ""):
        video.category = cate
    level = request.POST['level']
    if(level != ""):
        video.level = level
    time = request.POST['time']
    if(time != ""):
        video.time = time
    video.save()
    return redirect('video_edit_views', id=id)
