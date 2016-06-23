from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models.signals import post_save, pre_save 

# Create your models here.

class Venue(models.Model):
	name = models.CharField(max_length = 120, unique=True)
	slug = models.SlugField(unique=True, blank = True)
	rating = models.DecimalField(max_digits=9, decimal_places=6, blank = True)
	SPIRIT_TYPES = (
		('A', 'Alternative'),
		('B', 'Hipster'),
		('C', 'Chic'),
		('D', 'Local'),
		('E', 'Elegant'),
		('F', 'Tacky'),
	)
	spirit = models.CharField(max_length = 120, blank = True, choices = SPIRIT_TYPES)
	
	# Location
	location = models.CharField(max_length = 250, unique = False)
	lat = models.DecimalField(max_digits=14, decimal_places=10, default=0, blank = True)
	lng = models.DecimalField(max_digits=14, decimal_places=10, default=0, blank = True)

	def __str__(self):
		return str(self.name) + str(self.id)

	def get_absolute_url(self):
		return reverse("venue", kwargs={"slug": self.slug})

def create_venue_slug(instance, new_slug=None):
	if instance.name: 
		slug = slugify(instance.name)
	else:
		identifier = str(instance.name) + str(instance.id)
		slug = slugify(instance.name)
	if new_slug is not None:
		slug = new_slug
	qs = Venue.objects.filter(slug=slug).order_by("-id") 
	exists = qs.exists()  
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_venue(sender, instance, *args, **kwargs):
	instance.slug = slugify(instance.name)
pre_save.connect(pre_save_venue, sender = Venue)