from django.contrib import admin
from .models import EventGroup, Event, EventRequest

# Register your models here.

admin.site.register(Event)
admin.site.register(EventGroup)
admin.site.register(EventRequest)