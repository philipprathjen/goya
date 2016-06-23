from django.shortcuts import render, get_object_or_404
from urllib.parse import quote_plus
from .models import Venue

# Create your views here.
def venue(request, slug=None):
	instance = get_object_or_404(Venue, slug=slug)
	share_string = quote_plus(instance.name)
	context = {
		"share_string": share_string,
	}
	return render(request, "venues/venue.html", context)