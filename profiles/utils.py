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
from .models import School, Job, Place, UserLike, FbEvent, Match

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
		else:
			item.picture = "/static/img/profile_pics/profile_default.png"

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

		pager = fb_like_data['paging']['next']
		like_dict = fb_like_data['data']

		try: 
			pos = pager.find('after')
			pager = pager[:pos] + "after="
			print(pager) 
		except:
			pass

		before = fb_like_data['paging']['cursors']['before']
		after = fb_like_data['paging']['cursors']['after']
		while before:
			next_page= pager + before
			new_data = requests.get(next_page).json()
			like_list = new_data['data']
			for elem in like_list:
				like_dict.append(elem)
			try:
				before = new_data['paging']['cursors']['before']
			except:
				before=None

		while after:
			next_page= pager + after
			new_data = requests.get(next_page).json()
			like_list = new_data['data']
			for elem in like_list:
				like_dict.append(elem)
			try:
				after = new_data['paging']['cursors']['after']
			except:
				after=None
		try:
			likes={}
			for elem in like_dict:
				try: 
					like_name=str(elem['name'])
					like_id=str(elem['id'])			
					likes[like_name]=like_id
					item, created = UserLike.objects.get_or_create(fb_id = like_id)
					item.name = like_name
					item.save()
					profile.likes.add(item)
				except:
					pass
			print(likes, len(likes))
		except:
			pass
	except:
		likes = None
		pass
	return likes

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

		pager = fb_event_data['paging']['next']
		event_dict = fb_event_data['data']

		try: 
			pos = pager.find('after')
			pager = pager[:pos] + "after="
			print(pager) 
		except:
			pass

		before = fb_event_data['paging']['cursors']['before']
		after = fb_event_data['paging']['cursors']['after']
		while before:
			next_page= pager + before
			new_data = requests.get(next_page).json()
			event_list = new_data['data']
			for elem in event_list:
				event_dict.append(elem)
			try:
				before = new_data['paging']['cursors']['before']
			except:
				before=None

		while after:
			next_page= pager + after
			new_data = requests.get(next_page).json()
			event_list = new_data['data']
			for elem in event_list:
				event_dict.append(elem)
			try:
				after = new_data['paging']['cursors']['after']
			except:
				after=None
		try:
			events={}
			for elem in event_dict:
				try: 
					event_name=str(elem['name'])
					event_id=str(elem['id'])			
					events[event_name]=event_id
					item, created = FbEvent.objects.get_or_create(fb_id = event_id)
					item.name = event_name
					item.save()
					profile.events.add(item)
				except:
					pass
			print(events, len(likes))
		except:
			pass
	except:
		events = None
		pass

	return events


def get_matches(username):
	user_a = get_object_or_404(User, username=username)
	print('This is the user:', user_a)
	user_profile = Profile.objects.get(user = user_a)
	print('This is the user profile: ', user_profile)
	print(user_profile)
	queryset = Profile.objects.all()
	print(queryset)
	qset_likes_a = user_profile.likes.all()
	qset_events_a = user_profile.events.all()
	for profile in queryset:
		user_b = profile.user
		print(user_a, user_b)
		
		##### Common Likes
		qset_likes_b = profile.likes.all()
		print(type(qset_likes_a), type(qset_likes_b))
		set_likes_a = []
		for elem in qset_likes_a:
			set_likes_a.append(elem)
		set_likes_b = []
		for elem in qset_likes_b:
			set_likes_b.append(elem)
		common_likes = set(set_likes_a).intersection(set_likes_b)

		### Common Events
		qset_events_b = profile.events.all()
		set_events_a = []
		for elem in qset_events_a:
			set_events_a.append(elem)
		set_events_b = []
		for elem in qset_events_b:
			set_events_b.append(elem)
		common_events = set(set_events_a).intersection(set_events_b)
		print(common_events)

		##### Common Places

		##### Common Employer

		##### Common School
		
		##### Facebook Friends
		### Remember to add this to model directly


		##### Age difference


		##### Educational level


		


		##### Temporary Matching Algorithm:
		matching_score = len(common_likes) + len(common_events)
		print('This is the matching score: ', matching_score)


		##### Saving the match
		print('starting save')
		if user_a != user_b:
			item, created = Match.objects.get_or_create(user_a = user_a, user_b = user_b)
			print('got match from database')
			print('assigned the users')
			item.match_decimal = matching_score
			print('assigned matching_score')
			item.save()
			print('Done')
		else:
			pass

	return 'Matching Algorithm Complete'

# def social_score(username):




