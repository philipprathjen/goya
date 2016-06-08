from django.shortcuts import render, get_object_or_404
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

#Profile data
from .models import School, Job, Place

def update_fb_data(username):
	user = get_object_or_404(User, username=username)
	profile, created = Profile.objects.get_or_create(user=user)
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
		base_url = 'https://graph.facebook.com/v2.6/'
		basic_info = "{base_url}{fb_uid}?fields=id,name,birthday,picture,education,hometown,location,work&format=json".format(
			base_url = base_url,
			fb_uid = uid)
		plus_token = "{basic_info}&access_token={token}".format(basic_info = basic_info, token=token)
		fb_data = requests.get(plus_token).json()
	except:
		print('Epic fail')
		fb_data=None
		pass
	try:
		### Get and Save Image
		# print('The picture url: ', type(fb_data), fb_data['picture']['data']['url'])
		img_url = str(fb_data['picture']['data']['url'])
		urllib.request.urlretrieve(img_url, "../static/img/profile_pics/%s.jpg" %(fb_data['id']))
		item = Profile.objects.get(user=user)
		if img_url and not item.picture:
			#item = Profile(user_profile)
			item.picture = "/static/img/profile_pics/%s.jpg" %(fb_data['id'])
			item.save()

		### Get and Save Birthday
		birthday = fb_data['birthday']
		print('The birthday: ',birthday, type(birthday))
		year = birthday[6:]
		month = birthday[0:2]
		day =birthday[3:5]
		bday = '%s-%s-%s' %(year, month, day)
		print(bday)
		if profile.birthday != bday:
			profile.birthday = bday
			profile.save()


		### Get and Save Education
		education = fb_data['education']
		for edu in education:
			fbid = edu['school']['id']
			item, created = School.objects.get_or_create(fb_id = fbid)
			fb_name =edu['school']['name']
			fb_type = edu['type']
			item.school_type = fb_type
			item.name = fb_name
			item.save()
			profile.schools.add(item)
		
		### Get and Save Work
		work = fb_data['work']
		for job in work:
			fbid = job['employer']['id']
			fb_name = job['employer']['name']
			item, created = Job.objects.get_or_create(fb_id = fbid)
			item.fb_id = fbid
			item.name = fb_name
			item.save()
			profile.jobs.add(item)

		### Get and Save Places
		current_city = fb_data['location']
		fbid = current_city['id']
		item, created = Place.objects.get_or_create(fb_id = fbid)
		item.name = current_city['name']
		item.fb_id = fbid
		item.save()
		hometown = fb_data['hometown']
		fbid =hometown['id']
		item, created = Place.objects.get_or_create(fb_id = fbid)
		item.name = hometown['name']
		item.fb_id = fbid
		item.save()
	except:
		pass



	return fb_data

def update_friend_data(username):
	user = get_object_or_404(User, username=username)
	profile, created = Profile.objects.get_or_create(user=user)
	try: 
		fball = SocialAccount.objects.filter(provider = 'facebook')
		fbid = SocialAccount.objects.filter(
			user=user, 
			provider = 'facebook').first()
		print('this is it', fbid)
		social_token = SocialToken.objects.filter(
			account__user = user, 
			account__provider = 'facebook').first()
		uid = fbid.uid

		token = social_token.token
		base_url = 'https://graph.facebook.com/v2.6/'
		basic_info = "{base_url}{fb_uid}/friends?fields=id,name&format=json".format(
			base_url = base_url,
			fb_uid = uid)
		plus_token = "{basic_info}&access_token={token}".format(basic_info = basic_info, token=token)
		fb_friend_data = requests.get(plus_token).json()
	except:
		fb_friend_data = None
		pass
	return fb_friend_data

def update_like_data(username):
	user = get_object_or_404(User, username=username)
	profile, created = Profile.objects.get_or_create(user=user)
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
		base_url = 'https://graph.facebook.com/v2.6/'
		basic_info = "{base_url}{fb_uid}/likes?fields=total_count,id,name&format=json".format(
			base_url = base_url,
			fb_uid = uid)
		plus_token = "{basic_info}&access_token={token}".format(basic_info = basic_info, token=token)
		fb_like_data = requests.get(plus_token).json()
		print(fb_like_data)

	except:
		fb_like_data = None
		pass
	return fb_like_data

def update_event_data(username):
	user = get_object_or_404(User, username=username)
	profile, created = Profile.objects.get_or_create(user=user)
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
		base_url = 'https://graph.facebook.com/v2.6/'
		basic_info = "{base_url}{fb_uid}/events?fields=id,name&format=json".format(
			base_url = base_url,
			fb_uid = uid)
		plus_token = "{basic_info}&access_token={token}".format(basic_info = basic_info, token=token)
		fb_event_data = requests.get(plus_token).json()
		print('Events:', fb_event_data)

	except:
		fb_event_data = None
		pass
	return fb_event_data

def update_context_data(username):
	user = get_object_or_404(User, username=username)
	profile, created = Profile.objects.get_or_create(user=user)
	try: 
		fball = SocialAccount.objects.filter(provider = 'facebook')
		fbid = SocialAccount.objects.filter(
			user=user, 
			provider = 'facebook').first()
		print('First, this is it: ', fbid)
		social_token = SocialToken.objects.filter(
			account__user = user, 
			account__provider = 'facebook').first()
		uid = fbid.uid
		print('Does this work: ', uid)
		token = social_token.token
		print(social_token)
		base_url = 'https://graph.facebook.com/v2.6/'
		print(base_url)
		basic_info = "{base_url}{fb_uid}?fields=context&format=json".format(
			base_url = base_url,
			fb_uid = uid)
		print(basic_info)
		plus_token = "{basic_info}&access_token={token}".format(basic_info = basic_info, token=token)
		fb_context = requests.get(plus_token).json()
		print(fb_context.status_code)
		print(fb_context.json())
	except:
		fb_context = None
		print('Epic fail')
		pass
	return fb_context