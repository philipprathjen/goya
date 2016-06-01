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

@login_required
def my_events(request):
	user = request.user
	active_events = Event.objects.filter(active=True, creator=user)
	qs = EventGroup.objects.filter(event=active_events)
	instance = active_events[0]
	attend_form = AttendForm()
	

	try: 
		instance = qs[0]
		guests = instance.guests.all()
	except:
		guests = 'No guests'
	
	#url = instance.get_absolute_url()
	#print(url)
	requests = EventRequest.objects.filter(event=active_events)
	
	my_guests = {}
	my_requests = {}
	for instance in active_events:
		request_instance = EventRequest.objects.filter(event=instance)
		guest_req = []
		for attreq in request_instance:
			guest_req.append(attreq.get_guest())
		my_requests[instance] = guest_req
	print(my_requests, type(my_requests), guests)

	if request.method == 'POST':
		attend_form = AttendForm()
		event_id = request.POST['id']
		event_name = request.POST['name']
		guest = request.POST['guest']
		if attend_form.is_valid:
			try: 
				event = Event.objects.filter(id=event_id)[0]
				exist = EventGroup.objects.filter(event=event)
			except:
				exist = None
			if not exist: 
				attend_conf = EventGroup()
				event = Event.objects.filter(id=event_id)
				invite_user = User.objects.filter(username=guest)
				attend_conf.event = Event.objects.filter(id=event_id)[0]
				attend_conf.save()
				#attend_conf.guests = User.objects.filter(username=user)			
				user_attend = User.objects.filter(username=guest)[0]
				attend_conf.guests.add(user_attend)
				# try:
				# 	attend_conf.create()
				# except:
				# 	attend_conf.save()
			else: 
				group = exist[0]
				user_attend = User.objects.filter(username=guest)[0]
				group.guests.add(user_attend)


	context = {
	'user': user,
	'active_events': active_events,
	'guests': guests,
	'requests': requests,
	'attend_form': attend_form,
	'my_requests': my_requests,
	}
	return render(request, "events/my_events.html", context)

def new_event(request):
	user_data = {'creator': request.user}
	new_event_form=EventForm(user_data)
	context = {
	'new_event_form': new_event_form,
	}
	return render(request, "events/create_event.html", context)

def create_success(request):
	if request.method=='POST':
		event_form = EventForm()
		creator = request.POST['creator']
		name = request.POST['name']
		slug = request.POST['slug']
		num_people = request.POST['num_people']
		event_type = request.POST['event_type']
		location = request.POST['location']
		max_invit = request.POST['max_invit']
		num_girl = request.POST['num_girl']
		num_boy = request.POST['num_boy']
		sp_score_req = request.POST['sp_score_req']
		byo = request.POST['byo']
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

