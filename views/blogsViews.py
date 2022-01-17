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
from views.videosViews import pagination_result


def blogs_upload_views(request):
    if not request.user.is_authenticated:
        return redirect('user_login_views')
    return render(request, 'client/views/blogs_upload_views.html')



def blogs_upload_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        desc = request.POST['desc']
        body = request.POST['body']
        thumb_nail = request.FILES['thumbnail_img']
        cate = request.POST['category']
        user_obj = User.objects.get(username=request.user)
        post = Blog(author=user_obj, title=title, desc=desc, thumbnail=thumb_nail, body=body, category=cate)
        post.save()
        messages.success(request, 'Bạn đã tạo bài viết thành công!.')
    return redirect('blogs_upload_views')


def blog_detail_views(request, blog_id):
    if not request.user.is_authenticated:
        return redirect('user_login_views')
    try:
        blog_obj = Blog.objects.get(id=blog_id)
    except ObjectDoesNotExist:
        return render(request, '404.html')
    session_obj = User.objects.get(username = request.user.username)
    #blog_comment = Comment.objects.filter(post=blog_obj).order_by('-id')
    is_liked = False
    if session_obj in blog_obj.likes.all():
        is_liked = True
    else:
        is_liked = False
    params = {'blog':blog_obj,'is_liked':is_liked}
    return render(request, 'client/views/blog_detail_views.html', params)

def blogs_list_views(request, page=1):
    if not request.user.is_authenticated:
        return redirect('user_login_views')
    item_per_page = 10
    total_item = Blog.objects.count()
    total_page = math.floor(total_item / item_per_page)
    pagination = pagination_result(page, item_per_page, total_page)
    blogs_post = Blog.objects.order_by('-id').all()[pagination[1]: pagination[2]]
    for item in blogs_post:
        item.pub_date = item.pub_date.strftime("%d/%m/%Y")
    params = {
        'blogs': blogs_post,
        'total': range(1, total_page + 1),
        'page': page}
    return render(request, 'client/views/blogs_list_views.html', params)


