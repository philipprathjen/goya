from django.contrib import admin
from .models import Profile, School, Job, Place, FbEvent, UserLike, Match
# Register your models here.

admin.site.register(Profile)
admin.site.register(School)
admin.site.register(Job)
admin.site.register(Place)
admin.site.register(FbEvent)
admin.site.register(UserLike)
admin.site.register(Match)