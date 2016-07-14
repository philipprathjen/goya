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

#time handling
from datetime import datetime, timezone, timedelta

# The Facebook tools
from .utils import update_fb_data, update_friend_data, update_like_data, update_event_data, get_matches


@login_required
def profile_view(request, username):
	print('This is the username:', username, type(username))
	user = get_object_or_404(User, username=username)
	print(user)
	profile, created = Profile.objects.get_or_create(user=user)
	updated = profile.updated
	now = datetime.now(timezone.utc)
	
	#### Load CSS
	profile_css = True
	
	#### Facebook data stuff
	
	print(now-profile.updated)
	time_diff = now - profile.updated
	if time_diff > timedelta(days=30):
		try:
			fb_data = update_fb_data(username)
		except:
			fb_data=None
		try:
			fb_friend_data = update_friend_data(username)
		except:
			fb_friend_data=None
		try:
			fb_like_data = update_like_data(username)
		except:
			fb_like_data=None
		try:	
			fb_event_data = update_event_data(username)
		except:
			fb_event_data=None
		try:
			matches = get_matches(username)
		except:
			matches = None


		context = {
			'profile': profile,
			'fb_data':fb_data,
			'fb_friend_data': fb_friend_data,
			'fb_like_data': fb_like_data,
			'fb_event_data': fb_event_data,
			'matches': matches,
			'profile_css': profile_css,
			}
	else:
		context = {
			'profile': profile,
			'profile_css': profile_css,
		}

	print(profile.jobs.all())
	return render(request, 'profiles/profile_view.html', context)
