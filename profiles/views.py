from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth import get_user_model 
from django.http import Http404

User = get_user_model()

@login_required
def profile_view(request, username):
	user = get_object_or_404(User, username=username)
	profile, created = Profile.objects.get_or_create(user=user)
	context = {
		'profile': profile,
		}

	return render(request, 'profiles/profile_view.html', context)
