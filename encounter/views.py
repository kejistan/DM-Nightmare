# Create your views here.
from django.views.generic import list_detail, create_update
from django.shortcuts import get_object_or_404, render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from encounter.models import *
from encounter.forms import *

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
    return create_update.create_object(request, model=Action,
                                       post_save_redirect=redirect_to,
                                       *args, **kwargs)

def creature_instance_action_create(request, creatureinstance_id, *args,
                                    **kwargs):
    creature = get_object_or_404(CreatureInstance, pk=creatureinstance_id)
    if request.method == 'POST':
        action = Action(target=creature)
        action_form = ActionForm_Creatureless(request.POST, instance=action)
        if action_form.is_valid():
            action_form.save()
            redirect_to = creature.encounter.get_absolute_url()
            return HttpResponseRedirect(redirect_to)
    else:
        action_form = ActionForm_Creatureless()

    kwargs.update(csrf(request))
    c = dict(form=action_form, **kwargs)
    return render_to_response('encounter/action_form.html', c)

def encounter_creature_create(request, encounter_id, *args, **kwargs):
    e = get_object_or_404(Encounter, pk=encounter_id)
    if request.method == 'POST':
        c = CreatureInstance(encounter=e)
        creature_form = CreatureInstanceForm_Encounterless(request.POST,
                                                           instance=c)
        if creature_form.is_valid():
            creature_form.save()
            redirect_to = e.get_absolute_url()
            return HttpResponseRedirect(redirect_to)
    else:
        creature_form = CreatureInstanceForm_Encounterless()

    kwargs.update(csrf(request))
    context = dict(form=creature_form, **kwargs)
    return render_to_response('encounter/creatureinstance_form.html',
                              context)
