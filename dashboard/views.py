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



@login_required
def dashboard(request):
	user = request.user
	active_events = Event.objects.filter(active=True).exclude(creator=user)
	requested_events = EventRequest.objects.filter(guest=user)

	print(requested_events)
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
		print(instance.event)
		active_events = active_events.exclude(eventrequest = instance.id)


	context = {
		'user': user,
		'active_events': active_events,
		'request_form': request_form,
	}
	return render(request, "dashboard/dashboard.html", context)

def about(request):
	return render(request, "about.html", {})