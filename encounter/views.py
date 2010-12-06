# Create your views here.
from django.views.generic import list_detail, create_update
from django.shortcuts import get_object_or_404
from encounter.models import Encounter, CreatureClass, CreatureInstance, Action

def encounter_creature_list(request, object_id):
    creatures = get_object_or_404(Encounter, pk=object_id).creatures.all()
    return list_detail.object_list(request, queryset=creatures)

def encounter_action_list(request, encounter_id):
    actions = get_object_or_404(Encounter, pk=encounter_id).actions.all()
    extra = { 'encounter_id' : encounter_id }
    return list_detail.object_list(request, queryset=actions,
                                   extra_context=extra)

def encounter_action_create(request, encounter_id, *args, **kwargs):
    encounter = get_object_or_404(Encounter, pk=encounter_id)
    redirect_to = encounter.get_absolute_url()
    return create_update.create_object(request,
                                       model=Action,
                                       post_save_redirect=redirect_to,
                                       *args, **kwargs)

def creature_instance_action_create(request, creatureinstance_id, *args,
                                    **kwargs):
    creatureinstance = get_object_or_404(CreatureInstance,
                                         pk=creatureinstance_id)
    redirect_to = creatureinstance.get_absolute_url()
    return create_update.create_object(request, model=Action,
                                       post_save_redirect=redirect_to,
                                       *args, **kwargs)
