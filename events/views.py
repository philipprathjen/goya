from django.shortcuts import render, get_object_or_404
from urllib.parse import quote_plus

# Authentication
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model 
from profiles.models import Profile
from django.conf import settings
#User = settings.AUTH_USER_MODEL
User = get_user_model()

# Event Models and Forms 
from .models import Event, EventGroup, EventRequest
from .forms import EventForm, AttendForm
from venues.models import Venue

# Geolocation
from geopy import geocoders

@login_required
def my_events(request):
	user = request.user
	if request.method == 'POST':
		attend_form = AttendForm()
		event_id = request.POST['id']
		event_name = request.POST['name']
		guest = request.POST['guest']
		try:
			decline = request.POST['decline']
		except:
			decline = None
		if attend_form.is_valid and not decline:
			try: 
				event = Event.objects.filter(id=event_id)[0]
				exist = EventGroup.objects.filter(event=event)
			except:
				exist = None
			if not exist: 
				attend_conf = EventGroup()
				event = Event.objects.filter(id=event_id)
				attend_conf.event = Event.objects.filter(id=event_id)[0]
				attend_conf.save()
				#attend_conf.guests = User.objects.filter(username=user)			
				user_attend = User.objects.filter(username=guest)[0]
				attend_conf.guests.add(user_attend)
			else: 
				group = exist[0]
				user_attend = User.objects.filter(username=guest)[0]
				group.guests.add(user_attend)			
			EventRequest.objects.filter(event=event, guest=user_attend).delete()
		if attend_form.is_valid and decline:
			event = Event.objects.filter(id=event_id)[0]
			user_attend = User.objects.filter(username=guest)[0]
			EventRequest.objects.filter(event=event, guest=user_attend).delete()
	active_events = Event.objects.filter(active=True, creator=user)
	qs = EventGroup.objects.filter(event=active_events)
	try: 
		instance = active_events[0]
		url = instance.get_absolute_url()
	except:
		pass
	attend_form = AttendForm()
	my_guests = {}
	for instance in active_events:
		try:
			request_instance = EventRequest.objects.filter(event=instance)
			guest_req = []
			for attreq in request_instance:
				elem = attreq.get_guest()
				print(elem)
				visitor = Profile.objects.get(user=elem)
				print(visitor, type(visitor))
				guest_req.append(visitor)
			my_guests[instance] = {'requests': guest_req} 
		except:
			pass

	#### Show attending guests
	for instance in active_events:
		try:
			guest_list = []
			attending = EventGroup.objects.get(event=instance)
			print('This is attending: ', attending)
			guests_qs = attending.guests.all()
			for user_elem in guests_qs:
				visitor = Profile.objects.get(user=user_elem)
				guest_list.append(visitor)
			my_guests[instance] = {'attending': guest_list}
		except:
			pass		

	context = {
	'user': user,
	'active_events': active_events,
	'attend_form': attend_form,
	'my_guests': my_guests,
	}
	return render(request, "events/my_events.html", context)


def my_invitations(request):
	user = request.user
	event_invitations = EventGroup.objects.all()
	qs_events=[]
	for event in event_invitations:
		try:
			elem= Event.objects.filter(eventgroup=event, active=True)[0]
			qs_events.append(elem)
		except:
			pass
	events=[]
	for i in range(0,len(qs_events)):
		instance = qs_events[i]
		print(instance, instance.name)
		events.append(instance.name)


	# try: 
	# 	instance = qs
	# 	events = instance.events.all()
	# except:
	# 	events = 'No Invitations'

	context = {
	'user': user,
	'events': events
	}
	return render(request, "events/my_invitations.html", context)


def new_event(request):
	user_data = {'creator': request.user}
	creator = request.user
	new_event_form=EventForm(user_data)
	venues = Venue.objects.all()
	venue_dict = {}
	create_css = True
	for venue in venues:
		venue_dict[venue.id]=venue.name
	print(venue_dict)
	context = {
	'venues': venues,
	'venue_dict': venue_dict,
	'creator': creator, 
	'new_event_form': new_event_form,
	'create_css': create_css,
	}
	return render(request, "events/create_event.html", context)

def create_success(request):
	if request.method=='POST':
		event_form = EventForm()
		creator = request.POST['creator']
		name = request.POST['name']
		slug = request.POST['slug']
		num_people = request.POST['num_people']
		date = request.POST['date']
		time = request.POST['time']
		print(date, time)
		datetime = str(date) + ' ' + str(time)
		try:
			event_type = request.POST['event_type']
		except:
			event_type = 'H'
		location_entry = str(request.POST['location'])
		try:
			geolocator = geocoders.GoogleV3()
			location, (lat, lng) = geolocator.geocode(location_entry, timeout=20)
		except:
			location = request.POST['location']
		max_invit = request.POST['max_invit']
		try:
			num_girl = request.POST['num_girl']
			num_boy = request.POST['num_boy']
			sp_score_req = request.POST['sp_score_req']
		except:
			num_girl = 0
			num_boy = 0
			sp_score_req = 0
		try:
			byo = request.POST['byo']
			print(byo)
		except:
			byo=False
			print(byo)
		cash = request.POST['cash']
		other = request.POST['other']
		active = request.POST['active']
		if event_form.is_valid:
			event = Event()
			event.creator = request.user
			event.name = name
			event.slug = slug
			event.num_people = num_people
			event.event_type = event_type
			event.location = location
			event.max_invit = max_invit
			event.num_girl = num_girl
			event.num_boy = num_boy
			event.sp_score_req = sp_score_req
			event.byo = byo
			event.cash = cash
			event.other = other
			event.active = active
			event.event_time = datetime
			try: 
				#### getting the picture
				event.spirit_picture = picturefromhtml
			except:
				event.spirit_picture = "/media/static/img/spirit_pics/cocktail.jpg"
			try:
				event.lat = lat
				event.lng = lng
			except:
				pass
			try:
				event.create()
			except:
				event.save()

		context={
		}

		return render(request, "events/create_success.html", context)
	else:
		
		return render(request, "events/create_failure.html", context)

def events_detail(request, slug=None):
	instance = get_object_or_404(Event, slug=slug)
	print(instance)
	share_string = quote_plus(instance.name)
	context = {
		"name": instance.name,
		"instance": instance,
		"share_string": share_string,
	}
	return render(request, "events/events_detail.html", context)

