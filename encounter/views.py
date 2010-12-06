# Create your views here.
from django.views.generic import list_detail
from django.shortcuts import get_object_or_404
from encounter.models import Encounter, CreatureClass, CreatureInstance, Action

def encounter_creature_list(request, object_id):
    creatures = get_object_or_404(Encounter, pk=object_id).creatures.all()
    return list_detail.object_list(request, queryset=creatures)

def encounter_action_list(request, object_id):
    actions = get_object_or_404(Encounter, pk=object_id).actions.all()
    return list_detail.object_list(request, queryset=actions)
