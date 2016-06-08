from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.files import File

import os, sys, django
sys.path.append("/Users/philipp_rathjen/Documents/Work/Goya/goya/src")
os.environ["DJANGO_SETTINGS_MODULE"] = "goya.settings"
django.setup()


# Web Data Handling
import requests
import json
import urllib
from urllib.request import urlopen


# User Model and Auth Data
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth import get_user_model 
from allauth.socialaccount.models import SocialAccount, SocialToken
User = get_user_model()

from .utils import update_fb_data, update_friend_data, update_like_data, update_event_data, update_context_data


@login_required
def profile_view(request, username):
	print('This is the username:', username, type(username))
	user = get_object_or_404(User, username=username)
	print(user)
	profile, created = Profile.objects.get_or_create(user=user)
	fb_data=None
	fb_friend_data=None
	fb_like_data=None
	fb_event_data=None
	fb_context=None
	#### Facebook data stuff

	fb_data = update_fb_data(username)
	fb_friend_data = update_friend_data(username)
	fb_like_data = update_like_data(username)
	fb_event_data = update_event_data(username)
	fb_context = update_context_data(username)

	context = {
		'profile': profile,
		'fb_data':fb_data,
		'fb_friend_data': fb_friend_data,
		'fb_like_data': fb_like_data,
		'fb_event_data': fb_event_data,
		'fb_context': fb_context,
		}

	return render(request, 'profiles/profile_view.html', context)
