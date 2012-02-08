# -*- coding: utf-8 -*-
from django.core.context_processors import csrf
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
import datetime
from TZ.posts.models import Post, Coment
from django.contrib import auth
from django.contrib.auth.views import login, logout
from django.contrib.auth.models import User
from django.db import *
from django.conf.urls.defaults import *
from django.template.defaulttags import url
	

def Create(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")
	error_len_title = False
	necessary_forms_are_empty = False
	if ('title' and 'content') in request.GET:
		title = request.GET['title']
		content = request.GET['content']
		if 'coments_permission' in request.GET:
			coments_permission = request.GET['coments_permission']
		else: coments_permission = False
		if (len(title) > 250):
			error_len_title = True
			title = "";
			return render_to_response('create.html', locals())
		if (title <> "" and content <> ""):	
				post = Post(title=title, content=content, user=request.user, coments_permission=coments_permission)
				post.save()
				return HttpResponseRedirect("/myposts/")
		else:
			necessary_forms_are_empty = True
			return render_to_response('create.html', locals())	
	return render_to_response('create.html', locals())

def Profile(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")
	error_len_fname = False
	error_len_lname = False
	error_len_email = False
	error_no_unique_email = False
	necessary_forms_are_empty = False
	if ('email') in request.GET:
		first_name = request.GET['first_name']
		last_name = request.GET['last_name']
		email = request.GET['email']
		if (len(first_name) > 30):
			error_len_fname = True
			first_name = "";
		if (len(last_name) > 30):
			error_len_lname = True
			last_name = "";
		if (len(email) > 30):
			error_len_email = True
			email = "";
		if (email <> ""):
			try:
				p = User.objects.get(email=email)
			except User.DoesNotExist:			
				user = User.objects.filter(username=request.user.username).update(first_name=first_name, last_name=last_name, email=email)
				return HttpResponseRedirect("/myposts/")	
			else:
				if (email == request.user.email):
					user = User.objects.filter(username=request.user.username).update(first_name=first_name, last_name=last_name, email=email)
					return HttpResponseRedirect("/myposts/")				
				else:
					error_no_unique_email = True
					return render_to_response('profile.html', locals())
		else:
			necessary_forms_are_empty = True
			return render_to_response('profile.html', locals())	
	return render_to_response('profile.html', locals())
	
def View_post(request, id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")
	error = False
	id_post = id
	view_post = Post.objects.get(id=id_post)
	coments = Coment.objects.filter(post=view_post).order_by("date")
	if ('content') in request.GET:
		coment_add = request.GET['content']
		if (len(coment_add) < 10):
			error = True
			return render_to_response('view.html', locals())
		if (coment_add <> ""):
			c = Coment(content=coment_add, post=view_post, user=request.user)
			c.save()			
		else:
			error = True
			return render_to_response('view.html', locals())
	return render_to_response('view.html', locals())		
		
def List_of_posts(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")
	users_name = True
	User_id = request.user.username
	posts = Post.objects.order_by("date")
	return render_to_response('list.html', locals())
	
def List_of_my_posts(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")
	users_name = False
	User_id = request.user.username
	posts = Post.objects.filter(user=request.user.id).order_by("date")
	return render_to_response('list.html', locals())	

def Login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/posts/")
	error = False
	if ('username1' and 'password1') in request.GET:
		username1 = request.GET['username1']
		password1 = request.GET['password1']
		User = auth.authenticate(username=username1, password=password1)
		if User is not None and User.is_active:
			error = False
			auth.login(request, User)
			return HttpResponseRedirect("/myposts/")
		else:
			error = True
			return render_to_response('login.html',
			{'error': error})	
	error = False	
	return render_to_response('login.html', {'error': error})
	
def Logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")
	
def Reg(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/posts/")
	error = False
	error_len_login = False
	error_len_fname = False
	error_len_lname = False
	error_len_email = False
	error_len_password = False
	error_no_unique_login = False
	error_no_unique_email = False
	necessary_forms_are_empty = False
	if ('username' and 'password1') in request.GET:
		username = request.GET['username']
		first_name = request.GET['first_name']
		last_name = request.GET['last_name']
		password = request.GET['password1']
		email = request.GET['email']
		if (len(username) > 30):
			error_len_login = True
			username = "";
		if (len(first_name) > 30):
			error_len_fname = True
			first_name = "";
		if (len(last_name) > 30):
			error_len_lname = True
			last_name = "";
		if (len(email) > 30):
			error_len_email = True
			email = "";
		if (len(password) > 30):
			error_len_password = True
			password = "";
		if (username <> "" and password <> "" and email <> ""):
			try:
				p = User.objects.get(username=username)
			except User.DoesNotExist:
				try:
					p = User.objects.get(email=email)
				except User.DoesNotExist:			
					user = User.objects.create_user(username=username,
						email=email,
						password=password)
					user = User.objects.filter(username=username).update(first_name=first_name, last_name=last_name)
					User_auth = auth.authenticate(username=username, password=password)
					auth.login(request, User_auth)
					return HttpResponseRedirect("/myposts/")	
				else:
					email = "";
					error_no_unique_email = True
					return render_to_response('register.html', locals())
			else:
				username = "";
				error_no_unique_login = True
				return render_to_response('register.html', locals())
		else:
			necessary_forms_are_empty = True
			return render_to_response('register.html', locals())						
	return render_to_response('register.html', locals())