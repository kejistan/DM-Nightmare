from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic import list_detail, create_update
from encounter.models import Encounter, CreatureClass, CreatureInstance, Action

admin.autodiscover()

encounters = { 'queryset' : Encounter.objects.all() }
creature_classes = { 'queryset' : CreatureClass.objects.all() }
creature_instances = { 'queryset' : CreatureInstance.objects.all() }
actions = { 'queryset' : Action.objects.all() }

urlpatterns = patterns('',
    # Example:
    # (r'^dm_nightmare/', include('dm_nightmare.foo.urls')),
    (r'^creatures/(?P<creatureinstance_id>\d+)/action/create',
     'encounter.views.creature_instance_action_create', {},
     'creature_instance_action_create'),
    (r'^creatures/(?P<object_id>\d+)', list_detail.object_detail,
     creature_instances, 'creature_instance_detail'),
    (r'^creatures/classes/(?P<object_id>\d+)', list_detail.object_detail,
     creature_classes, 'creature_class_detail'),
    (r'^creatures/create', create_update.create_object,
     dict(model=CreatureClass, post_save_redirect='/creatures'),
     'creature_class_create'),
    (r'^creatures', list_detail.object_list, creature_classes,
     'creature_class_list'),

    (r'^actions/(?P<object_id>\d+)', list_detail.object_detail, actions,
     'action_detail'),
    (r'^actions', list_detail.object_list, actions, 'action_list'),

    (r'^encounters/(?P<encounter_id>\d+)/creatures/create',
     'encounter.views.encounter_creature_create',
     {}, 'encounter_creature_create'),
    (r'^encounters/(?P<object_id>\d+)/creatures',
     'encounter.views.encounter_creature_list',
     {}, 'encounter_creature_list'),
    (r'^encounters/(?P<encounter_id>\d+)/actions/create',
     'encounter.views.encounter_action_create', {},
     'encounter_action_create'),
    (r'^encounters/(?P<encounter_id>\d+)/actions',
     'encounter.views.encounter_action_list',
     {}, 'encounter_action_list'),
    (r'^encounters/(?P<object_id>\d+)', list_detail.object_detail,
     encounters, 'encounter_detail'),
    (r'^encounters', list_detail.object_list, encounters, 'encounter_list'),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)
