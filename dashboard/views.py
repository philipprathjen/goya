# Templating
from django.shortcuts import render
from django.http import Http404
# Authentication and user data
from django.contrib.auth import get_user_model 
from django.contrib.auth.decorators import login_required
User = get_user_model()
# Event selection
from events.models import Event, EventGroup, EventRequest
from events.forms import EventForm, RequestForm
# Geolocation
from django.contrib.gis.geoip2 import GeoIP2
from geopy import geocoders
from ipware.ip import get_ip
from math import cos
# Timestamp
from datetime import datetime, timezone, timedelta
### Matches
from profiles.models import Match
from django.db.models import Q
### Selection Tools
from .utils import locationFilter


def dashboard(request):
	if not request.user.is_authenticated():
		context = {}
		return render(request, "dashboard/landing.html", context)
	else:	

		user = request.user
		active_events = Event.objects.filter(active=True).exclude(creator=user)

		### Deactivate the events that have expired #####
		now = datetime.now(timezone.utc)
		for event in active_events:
			time_diff = event.event_time-now
			if time_diff < timedelta(days=1):
				event.active = False
				event.save()
		# Reload
		active_events = Event.objects.filter(active=True).exclude(creator=user)

		### Filter those the User created
		eventgroup = EventGroup.objects.filter(guests=user)
		for event in eventgroup:
			active_events = active_events.exclude(eventgroup=event)
		
		### Filter the events the user cant request invite
		# Get user social score
		critical_score = -2 ###### This can be changed
		qs_matches = Match.objects.filter(user_a=request.user).exclude(match_decimal__gte=critical_score)
		# Only too low matches left. These are excluded
		for instance in qs_matches:
			active_events.exclude(creator=instance.user_b)

		print(qs_matches)


		# Get profiles of events created
		# Compare and exclude

		requested_events = EventRequest.objects.filter(guest=user)
		user_data = {'guest': request.user}
		request_form = RequestForm(user_data)
		
		##### Form to attend event and exclude if attending
		if request.method == 'POST':
			request_form = RequestForm()
			event = request.POST['id']
			if request_form.is_valid:
				attend_request = EventRequest()
				attend_request.event = Event.objects.filter(id=event)[0]
				attend_request.guest = request.user
				try:
					attend_request.create()
				except:
					attend_request.save()
		for instance in requested_events:
			active_events = active_events.exclude(eventrequest = instance.id)

		#### Location sepcific search ## GET request
		if request.method == 'GET': 
			try:
				location_entry = str(request.GET['location'])
				geolocator = geocoders.GoogleV3()
				location, (lat, lng) = geolocator.geocode(location_entry, timeout=20)
			except:
				ip = get_ip(request)
				print(ip)
				if ip:
				    try:
				    	city = g.city(ip)['city']
				    	geolocator = geocoders.GoogleV3()
				    	location, (lat, lng) = geolocator.geocode(city, timeout=20)
				    except:
				    	lat = 48.7758
				    	lng= 9.1829
			print(lat, lng)
		
		### Import the right CSS file (binary for header)
		dashboard_css = True

		#### Only show within range
		active_events = locationFilter(lat, lng, active_events)


		context = {
			'user': user,
			'active_events': active_events,
			'request_form': request_form,
			'lat': lat,
			'lng': lng,
			'dashboard_css': dashboard_css,
		}
		return render(request, "dashboard/dashboard.html", context)

def about(request):
	return render(request, "about.html", {})