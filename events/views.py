from django.shortcuts import render, get_object_or_404
from .models import Event, EventGroup, EventRequest

# Authentication
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model 
User = get_user_model()
from profiles.models import Profile

from .forms import EventForm

@login_required
def event(request):
	user = request.user
	active_events = Event.objects.filter(active=True, creator=user)
	qs = EventGroup.objects.filter(event=active_events)
	try: 
		instance = qs[0]
		guests = instance.guests.all()
	except:
		guests = 'No guests'
	
	requests = EventRequest.objects.filter(event=active_events)
	
	context = {
	'user': user,
	'active_events': active_events,
	'guests': guests,
	'requests': requests,
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