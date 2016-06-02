from django.shortcuts import render, get_object_or_404
from django.http import Http404
import requests

# User Model and Auth Data
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth import get_user_model 
from allauth.socialaccount.models import SocialAccount, SocialToken
User = get_user_model()

@login_required
def profile_view(request, username):
	user = get_object_or_404(User, username=username)
	profile, created = Profile.objects.get_or_create(user=user)
	fb_data=None
	#### Facebook data stuff
	
	try: 
		fball = SocialAccount.objects.filter(provider = 'facebook')
		fbid = SocialAccount.objects.filter(
			user=user, 
			provider = 'facebook').first()
		social_token = SocialToken.objects.filter(
			account__user = user, 
			account__provider = 'facebook').first()
		uid = fbid.uid
		token = social_token.token
		base_url = 'https://graph.facebook.com/v2.5/'
		for u in fball: 
			basic_info = "{base_url}{fb_uid}?fields=id,name,picture,education,work&format=json".format(
				base_url = base_url,
				fb_uid = u.uid)
			plus_token = "{basic_info}&access_token={token}".format(basic_info = basic_info, token=token)
			fb_data = requests.get(plus_token).json()
			print(r.status_code)
			print(r.json())
	except:
		pass

	try: 
		fball = SocialAccount.objects.filter(provider = 'facebook')
		fbid = SocialAccount.objects.filter(
			user=user, 
			provider = 'facebook').first()
		social_token = SocialToken.objects.filter(
			account__user = user, 
			account__provider = 'facebook').first()
		uid = fbid.uid
		token = social_token.token
		base_url = 'https://graph.facebook.com/v2.5/'
		for u in fball: 
			basic_info = "{base_url}{fb_uid}/friends?fields=id&format=json".format(
				base_url = base_url,
				fb_uid = u.uid)
			plus_token = "{basic_info}&access_token={token}".format(basic_info = basic_info, token=token)
			fb_friend_data = requests.get(plus_token).json()

	except:
		pass

	try: 
		fball = SocialAccount.objects.filter(provider = 'facebook')
		fbid = SocialAccount.objects.filter(
			user=user, 
			provider = 'facebook').first()
		social_token = SocialToken.objects.filter(
			account__user = user, 
			account__provider = 'facebook').first()
		uid = fbid.uid
		token = social_token.token
		base_url = 'https://graph.facebook.com/v2.5/'
		for u in fball: 
			basic_info = "{base_url}{fb_uid}/likes?fields=total_count&format=json".format(
				base_url = base_url,
				fb_uid = u.uid)
			plus_token = "{basic_info}&access_token={token}".format(basic_info = basic_info, token=token)
			fb_like_data = requests.get(plus_token).json()

	except:
		pass

	context = {
		'profile': profile,
		'fb_data':fb_data,
		'fb_friend_data': fb_friend_data,
		'fb_like_data': fb_like_data,
		}

	return render(request, 'profiles/profile_view.html', context)
