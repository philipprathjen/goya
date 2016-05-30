# Templating
from django.shortcuts import render
from django.http import Http404
# Authentication and user data
from django.contrib.auth import get_user_model 
from django.contrib.auth.decorators import login_required

User = get_user_model()



# Create your views here.

def dashboard(request):
	user = request.user
	context = {
		'user': user,
	}
	return render(request, "dashboard/dashboard.html", context)