from django.conf.urls.defaults import patterns, include, url
from communeapp.models import Room
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
admin.site.register(Room)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'commune.views.home', name='home'),
    # url(r'^commune/', include('commune.foo.urls')),
    url(r'^$', 'communeapp.views.index'),
    url(r'^(?P<room_id>\d+)/$', 'communeapp.views.room'),
    url(r'^commune/(?P<room_id>\d+)/$', 'communeapp.views.room'),  #for testing purposes
    url(r'^submit$', 'communeapp.views.submit'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
