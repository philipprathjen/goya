from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models.signals import post_save, pre_save 
# pre_save will do sth prior to being saved. Right before the model is saved we're going to do something. 
from venues.models import Venue

# Create your models here.

User = settings.AUTH_USER_MODEL

### creat an add to group function

class Event(models.Model):
	# Basic Information
	creator = models.ForeignKey(User, related_name='event_creator')
	name = models.CharField(max_length = 120, unique=True)
	slug = models.SlugField(unique=True, blank = True)
	num_people = models.IntegerField(blank=False)
	EVENT_TYPES = (
		('B', 'BAR'),
		('H', 'HOUSE PARTY'),
		('C', 'CLUBBING'),
		('O', 'OTHER'),
	)
	event_type = models.CharField(max_length = 1, choices = EVENT_TYPES, blank=True)
	location = models.CharField(max_length = 250, unique = False)
	lat = models.DecimalField(max_digits=9, decimal_places=6, default=0, blank = True)
	lng = models.DecimalField(max_digits=9, decimal_places=6, default=0, blank = True)
	event_time = models.DateTimeField(auto_now=False, auto_now_add=False, blank=False, null=True)
	spirit_picture = models.ImageField(upload_to='static/img/spirit_pics/', null=True, blank = True)
	
	# Venue
	venue = models.ManyToManyField(Venue, blank=True)

	# Guest list
	max_invit = models.IntegerField(blank = False)
	num_girl = models.IntegerField(blank = True)
	num_boy = models.IntegerField(blank = True)
	sp_score_req = models.DecimalField(decimal_places=8, max_digits=16, default=0.00, blank=True)
	
	# Bring along
	byo = models.BooleanField(default = False)
	cash = models.IntegerField(blank = True, default = 0)
	other = models.CharField(max_length = 300, blank = True, unique=False)

	# Management
	active = models.BooleanField(default = True)
	timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
	updated = models.DateTimeField(auto_now_add = False, auto_now = True) 

	def __str__(self):
		return str(self.creator) + str(self.id)

	def get_absolute_url(self):
		return reverse("event_detail", kwargs={"slug": self.slug})

def create_slug(instance, new_slug=None):
	if instance.name: 
		slug = slugify(instance.name)
	else:
		identifier = str(instance.creator) + str(instance.id)
		slug = slugify(instance.name)
	if new_slug is not None:
		slug = new_slug
	qs = Event.objects.filter(slug=slug).order_by("-id") 
	exists = qs.exists()  
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_event(sender, instance, *args, **kwargs):
	instance.slug = slugify(instance.name)
pre_save.connect(pre_save_event, sender = Event)

class EventGroup(models.Model):
	event = models.ForeignKey(Event, null = True, blank=True)
	guests = models.ManyToManyField(User)

	def __str__(self):
		return str(self.id)

class EventRequest(models.Model):
	event = models.ForeignKey(Event, null = True, blank=True)
	guest = models.ForeignKey(User)

	def __str__(self):
		return str(self.id)

	def get_guest(self):
		return self.guest