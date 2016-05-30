from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

# For Signals
from django.db.models.signals import post_save, pre_save 
# Create your models here.

User = settings.AUTH_USER_MODEL

class Profile(models.Model):
	user = models.OneToOneField(User)
		# OneToOneField any user can only have one profile. Kind of a unique clause
	location = models.CharField(max_length = 120, null=True, blank=True)
	def __str__(self):
		return self.user.username

	def get_absolute_url(self):
		url = reverse('profile', kwargs={'username': self.user.username}) 
		#This actually gives us the URL
		return url