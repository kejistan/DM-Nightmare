from django.db import models

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

class CreatureInstance(models.Model):
    class = models.ForeignKey(CreatureClass, related_name='instances')
    
    def new_action(self, action):
        self.actions.create(dict(action, action_id=self.next_action_id()))

    def next_action_id(self):
        return self.actions.action_id_max + 1

class Action(models.Model):
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
    target = models.ForeignKey(CreatureInstance, related_name='actions')
    action_id = models.IntegerField()
