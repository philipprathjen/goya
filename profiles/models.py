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


class Profile(models.Model):
	user = models.OneToOneField(User)
		# OneToOneField any user can only have one profile. Kind of a unique clause
	location = models.CharField(max_length = 120, null=True, blank=True)
	picture = models.ImageField(upload_to='static/img/profile_pics/', null=True, blank = True)
	# events = models.ManyToManyField(Event)
	jobs = models.ManyToManyField(Job)
	schools = models.ManyToManyField(School)
	birthday = models.DateField(blank=True, null=True)
	# places = models.ManyToManyField(Place)
	# likes = models.ManyToManyField(UserLike)

	
	def __str__(self):
		return self.user.username

	def get_absolute_url(self):
		url = reverse('profile', kwargs={'username': self.user.username}) 
		#This actually gives us the URL
		return url

# class Event(models.Model):
# 	fb_id = models.CharField(max_length = 120, null=True, blank=True)
# 	name = models.CharField(max_length = 120, null=True, blank=True)






# class Place(models.Model):
# 	fb_id = models.CharField(max_length = 120, null=True, blank=True)
# 	name = models.CharField(max_length = 120, null=True, blank=True)

# class UserLike(models.Model):
# 	fb_id = models.CharField(max_length = 120, null=True, blank=True)
# 	name = models.CharField(max_length = 120, null=True, blank=True)
