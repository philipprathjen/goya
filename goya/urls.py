"""trydjango19 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # Dashboard and Auxiliary
    url(r'^$', 'dashboard.views.dashboard', name='landing'),
    url(r'^about/$', 'dashboard.views.about', name='about'),
    url(r'^posts/', include("posts.urls", namespace='posts')),
    
    # Profiles and Authentication
    url(r'^profile/(?P<username>[\w.@+-]+)/$', 'profiles.views.profile_view', name='profile'),
    url(r'^accounts/', include('allauth.urls')),
    #url(r'^posts/$', "<appname>.views.<function_name>"),

    # Events and Event Creation
    url(r'^my_events/$', 'events.views.my_events', name='my_events'),
    url(r'^invitations/$', 'events.views.my_invitations', name='my_invitations'),
    url(r'^create/$', 'events.views.new_event', name='new_event'),
    url(r'^create/success$', 'events.views.create_success', name='create_success'),
    url(r'^(?P<slug>[\w-]+)/$', 'events.views.events_detail', name='event_detail'),
    #url(r'(?P<id>\d+)/$', post_detail)
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)