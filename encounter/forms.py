from django.forms import ModelForm
from encounter.models import CreatureClass, CreatureInstance, Encounter, Action

class CreatureInstanceForm(ModelForm):
    class Meta:
        model = CreatureInstance

class CreatureInstanceForm_Classless(CreatureInstanceForm):
    class Meta(CreatureInstanceForm.Meta):
        exclude = ('creature_class',)

class CreatureInstanceForm_Encounterless(CreatureInstanceForm):
    class Meta(CreatureInstanceForm.Meta):
        exclude = ('encounter',)

class ActionForm(ModelForm):
    class Meta:
        model = Action

class ActionForm_Creatureless(ActionForm):
    class Meta(ActionForm.Meta):
        exclude = ('target',)
