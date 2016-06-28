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


def dashboard(request):
	if not request.user.is_authenticated():
		context = {}
		return render(request, "dashboard/landing.html", context)
	else:	

		user = request.user
		eventgroup = EventGroup.objects.filter(guests=user)
		active_events = Event.objects.filter(active=True).exclude(creator=user)
		for event in eventgroup:
			active_events = active_events.exclude(eventgroup=event)
		requested_events = EventRequest.objects.filter(guest=user)
		user_data = {'guest': request.user}
		request_form = RequestForm(user_data)
		
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

		# Google Map data
		

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
		context = {
			'user': user,
			'active_events': active_events,
			'request_form': request_form,
			'lat': lat,
			'lng': lng,
		}
		return render(request, "dashboard/dashboard.html", context)

def about(request):
	return render(request, "about.html", {})