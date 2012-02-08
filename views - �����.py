# -*- coding: utf-8 -*-
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render_to_response
import datetime
from TZ.posts.models import Post, Coment
from django.contrib import auth

def hello(request):
    return HttpResponse("Hello")
	
def current_datetime(request):
    current_date = datetime.datetime.now()
    return render_to_response('current_datetime.html', locals())
	
def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)
	
def search_form(request):
    return render_to_response('search_form.html')

def search(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            posts = Post.objects.filter(title__icontains=q)
            return render_to_response('search_results.html',
                {'posts': posts, 'query': q})
    return render_to_response('search_form.html',
        {'error': error})

		
def list_of_posts(request):
	posts = Post.objects.all()
	return render_to_response('list.html', locals())

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Правильный пароль и пользователь "активен"
        auth.login(request, user)
        # Перенаправление на "правильную" страницу
        return HttpResponseRedirect('list.html')
    else:
        # Отображение страницы с ошибкой
        return render_to_response('login.html',
        {'error': error})

def logout(request):
    auth.logout(request)
    # Перенаправление на страницу.
    return HttpResponseRedirect("/account/loggedout/")