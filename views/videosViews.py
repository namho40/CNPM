
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


def video_list_views(request, page=1):
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
    return render(request, 'client/views/video_list_views.html', params)


def video_detail_views(request, video_id):
    if not request.user.is_authenticated:
        return redirect('user_login_views')
    try:
        video_obj = VideoPost.objects.get(id=video_id)
    except ObjectDoesNotExist:
        return render(request, '404.html')
    try:
        session_obj = User.objects.get(username=request.user.username)
    except:
        messages.warning(request, 'You are not login to watch this video.')
        return redirect('homeDefault')

    video_comments = Comment.objects.filter(post=video_obj).order_by('-id')

    # Increase Views of Video if User visit this page
    if request.user not in video_obj.video_views.all():
        video_obj.video_views.add(request.user)
    # Increase Likes of Video if User like this video
    is_liked = False
    if session_obj in video_obj.likes.all():
        is_liked = True
    else:
        is_liked = False
    created_by = User.objects.get(id=video_obj.user_id)
    # print(video_obj.video_views)
    params = {'video': video_obj,
              'comments': video_comments,
              'is_liked': is_liked,
              'created_by': created_by,
              'video_views': video_obj.video_views.count()
              }
    return render(request, 'client/views/video_detail_views.html', params)


def video_upload_views(request):
    if not request.user.is_authenticated:
        return redirect('user_login_views')
    return render(request, 'client/views/video_upload_views.html')


def video_upload_post(request):
    if not request.user.is_authenticated:
        return redirect('user_login_views')
    if request.method == 'POST':
        title = request.POST['title']
        desc = request.POST['desc']
        video_file = request.FILES['fileName']
        thumb_nail = request.FILES['thumbnail_img']
        cate = request.POST['category']
        level = request.POST['level']
        time = request.POST['time']

        user_obj = User.objects.get(username=request.user)
        upload_video = VideoPost(user=user_obj, title=title, desc=desc, video_file=video_file,
                                 thumbnail=thumb_nail, category=cate, level=level, time=time)
        upload_video.save()
        messages.success(request, 'Bạn đã tạo công thức thành công')
    return redirect('video_upload_views')
