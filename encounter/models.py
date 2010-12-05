from django.db import models

class Encounter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    
    def new_creature(self, _class):
        return self.creatures.create(creature_class=_class)

class CreatureClass(models.Model):
    name = models.CharField(max_length=50)
    minimum_hp = models.IntegerField(blank=True)
    maximum_hp = models.IntegerField(blank=True)
    minimum_ac = models.IntegerField(blank=True)
    maximum_ac = models.IntegerField(blank=True)
    minimum_fort = models.IntegerField(blank=True)
    maximum_fort = models.IntegerField(blank=True)
    minimum_ref = models.IntegerField(blank=True)
    maximum_ref = models.IntegerField(blank=True)
    minimum_will = models.IntegerField(blank=True)
    maximum_will = models.IntegerField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _range(min, max):
        if (min == max):
            return str(max)
        else:
            return '[%d,%d]' % (min, max)

    def hp(self):
        return _range(self.minimum_hp, self.maximum_hp)

    def ac(self):
        return _range(self.minimum_ac, self.maximum_ac)

    def fort(self):
        return _range(self.minimum_fort, self.maximum_fort)

    def ref(self):
        return _range(self.minimum_ref, self.maximum_ref)

    def will(self):
        return _range(self.minimum_will, self.maximum_will)

    def new_instance(self, encounter):
        return encounter.new_creature(self.pk)

class CreatureInstance(models.Model):
    creature_class = models.ForeignKey(CreatureClass, related_name='instances')
    encounter = models.ForeignKey(Encounter, related_name='creatures')
    encounter_label = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def new_action(self, action):
        return self.actions.create(action)

    def clean_encounter_label(self):
        label = self.cleaned_data['encounter_label']
        try:
            if (self.encounter.creatures.get(encounter_label=label).pk != self.pk):
                return label
            else:
                raise forms.ValidationError('label already exists in encounter %d' % self.encounter.pk)
        except ObjectDoesNotExist:
            return label

class Action(models.Model):
    target = models.ForeignKey(CreatureInstance, related_name='actions')
    attack_roll = models.IntegerField()
    hit_status = models.BooleanField()
    attack_vs = models.IntegerField(choices=(
            (0, 'AC'),
            (1, 'FORT'),
            (2, 'REF'),
            (3, 'WILL'))
    )
    damage_roll = models.IntegerField()
    status_change = models.IntegerField(choices=(
            (0, 'no change'),
            (1, 'became bloodied'),
            (2, 'became dead'))
    )
    created_at = models.DateTimeField(auto_now_add=True)
