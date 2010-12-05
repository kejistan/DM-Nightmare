from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic import list_detail
from encounter.models import Encounter, CreatureClass

admin.autodiscover()

encounters = { 'queryset' : Encounter.objects.all() }
creature_classes = { 'queryset' : CreatureClass.objects.all() }

urlpatterns = patterns('',
    # Example:
    # (r'^dm_nightmare/', include('dm_nightmare.foo.urls')),
    (r'^encounters/creatures/', list_detail.object_list, creature_classes, 'creature_class_list'),
    (r'^encounters/(?P<object_id>\d+)/', list_detail.object_detail,
     encounters, 'encounter_detail'),
    (r'^encounters/', list_detail.object_list, encounters, 'encounter_list'),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)
