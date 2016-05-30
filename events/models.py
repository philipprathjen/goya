from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_save, pre_save
# Create your models here.

User = settings.AUTH_USER_MODEL

### creat an add to group function

class Event(models.Model):
	# Basic Information
	creator = models.ForeignKey(User, related_name='event_creator')
	name = models.CharField(max_length = 120, unique=True)
	slug = models.SlugField()
	num_people = models.IntegerField(blank=False)
	EVENT_TYPES = (
		('B', 'BAR'),
		('H', 'HOUSE PARTY'),
		('C', 'CLUBBING'),
		('O', 'OTHER'),
	)
	event_type = models.CharField(max_length = 1, choices = EVENT_TYPES)
	location = models.CharField(max_length = 250, unique = True)
	
	# Guest list
	max_invit = models.IntegerField(blank = False)
	num_girl = models.IntegerField(blank = True)
	num_boy = models.IntegerField(blank = True)
	sp_score_req = models.DecimalField(decimal_places=8, max_digits=16, default=0.00)
	
	# Bring along
	byo = models.BooleanField(default = False)
	cash = models.IntegerField(blank = True, default = 0)
	other = models.CharField(max_length = 300, unique = True, blank = True)

	# Management
	active = models.BooleanField(default = True)
	timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
	updated = models.DateTimeField(auto_now_add = False, auto_now = True) 

	def __str__(self):
		return str(self.creator) + str(self.id)

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