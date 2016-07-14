from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

# For Signals
from django.db.models.signals import post_save, pre_save 
# Create your models here.

User = settings.AUTH_USER_MODEL

class School(models.Model):
	fb_id = models.CharField(max_length = 120, null=True, blank=True, unique=True)
	school_type = models.CharField(max_length = 120, null=True, blank=True)
	name = models.CharField(max_length = 120, null=True, blank=True)
	def __str__(self):
		return self.name

class Job(models.Model):
	fb_id = models.CharField(max_length = 120, null=True, blank=True, unique=True)
	name = models.CharField(max_length = 120, null=True, blank=True)
	def __str__(self):
		return self.name

class Place(models.Model):
	fb_id = models.CharField(max_length = 120, null=True, blank=True)
	name = models.CharField(max_length = 120, null=True, blank=True)
	def __str__(self):
		return self.name
class FbEvent(models.Model):
	fb_id = models.CharField(max_length = 120, null=True, blank=True)
	name = models.CharField(max_length = 200, null=True, blank=True)
	def __str__(self):
		return self.name
class UserLike(models.Model):
	fb_id = models.CharField(max_length = 120, null=True, blank=True)
	name = models.CharField(max_length = 200, null=True, blank=True)
	def __str__(self):
		return self.name

class Profile(models.Model):
	user = models.OneToOneField(User)
		# OneToOneField any user can only have one profile. Kind of a unique clause
	location = models.CharField(max_length = 120, null=True, blank=True)
	picture = models.ImageField(upload_to='static/img/profile_pics/', null=True, blank = True)
	events = models.ManyToManyField(FbEvent, blank=True)
	jobs = models.ManyToManyField(Job, blank=True)
	schools = models.ManyToManyField(School, blank=True)
	birthday = models.DateField(blank=True, null=True)
	places = models.ManyToManyField(Place, blank=True)
	likes = models.ManyToManyField(UserLike, blank=True)
	
	# Management
	active = models.BooleanField(default = True)
	timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
	updated = models.DateTimeField(auto_now_add = False, auto_now = True) 

	
	def __str__(self):
		return self.user.username

	def get_absolute_url(self):
		url = reverse('profile', kwargs={'username': self.user.username}) 
		#This actually gives us the URL
		return url

class Match(models.Model):
	user_a = models.ForeignKey(User, related_name= 'match_user_a')
	user_b = models.ForeignKey(User, related_name= 'match_user_b')
	fb_match = models.BooleanField(default = False)
	match_decimal = models.DecimalField(decimal_places=8, max_digits=16, default=0.00)
	timestamp = models.DateTimeField(auto_now_add = True, auto_now = False)
	updated = models.DateTimeField(auto_now_add = False, auto_now = True)

	def __str__(self):
		return "%s-%s" %(self.user_a, self.user_b)


