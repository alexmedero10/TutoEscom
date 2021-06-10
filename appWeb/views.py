from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import UserRegisterForm, UserImageForm, PostForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import os

def feed(request):
	posts = Post.objects.all()

	context = { 'posts': posts}
	return render(request, 'feed.html', context)

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		profile_form = UserImageForm(request.POST, request.FILES)
		if form.is_valid() and profile_form.is_valid():
			user = form.save()
			profile_form = profile_form.save(commit=False)
			profile_form.user = user
			if 'image' in request.FILES:
				profile_form.image = request.FILES['image']
			profile_form.save()
			username = form.cleaned_data['username']
			messages.success(request, f'Usuario {username} creado')
			return redirect('feed')
	else:
		form = UserRegisterForm()
		profile_form = UserImageForm()

	context = { 'form' : form, 'profile_form': profile_form}
	return render(request, 'register.html', context)

@login_required
def post(request):
	current_user = get_object_or_404(User, pk=request.user.pk)
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = current_user
			post.save()
			messages.success(request, 'Post enviado')
			return redirect('feed')
	else:
		form = PostForm()
	return render(request, 'post.html', {'form' : form })

def like(request, post_id):
	user = User.objects.get(username=request.user.username)
	post = Post.objects.get(id=post_id)

	newLike = Like(user=user, post=post)
	newLike.alreadyLiked = True

	post.likes += 1
	#adds user to Post 
	post.user_likes.add(user)
	post.save()
	newLike.save()
	messages.success(request, f'Te gusta la publicación')
	return redirect('feed')

def dislike(request, post_id):
	user = User.objects.get(username=request.user.username)
	post = Post.objects.get(id=post_id)
	deleteLike = Like.objects.filter(user=user.id, post=post.id).get()
	post.user_likes.remove(user)
	post.likes -= 1
	post.save()
	#delete user from Post 
	deleteLike.delete()
	messages.success(request, f'Ya no te gusta la publicación')
	return redirect('feed')

def profile(request, username=None):
	current_user = request.user
	if username and username != current_user.username:
		user = User.objects.get(username=username)
		posts = user.posts.all()
	else:
		posts = current_user.posts.all()
		user = current_user
	return render(request, 'profile.html', {'user':user, 'posts':posts})


def follow(request, username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user
	rel = Relationship(from_user=current_user, to_user=to_user_id)
	rel.save()
	messages.success(request, f'sigues a {username}')
	return redirect('feed')

def unfollow(request, username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user.id
	rel = Relationship.objects.filter(from_user=current_user.id, to_user=to_user_id).get()
	rel.delete()
	messages.success(request, f'Ya no sigues a {username}')
	return redirect('feed')
