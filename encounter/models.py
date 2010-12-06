from django.db import models

def _range(min, max):
    if (min == max):
        return str(max)
    else:
        return '[%s,%s]' % (str(min), str(max))

_AC = 0
_FORT = 1
_REF = 2
_WILL = 3
_NO_CHANGE = 0
_BLOODIED = 1
_DEAD = 2

class Encounter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def actions(self):
        return Action.objects.filter(target__in=self.creatures.all()).distinct()
    
    def new_creature(self, _class):
        return self.creatures.create(creature_class=_class)

    def __unicode__(self):
        return unicode(self.created_at)

    @models.permalink
    def get_absolute_url(self):
        return ('encounter_detail', (),
                { 'object_id' : self.pk })

class CreatureClass(models.Model):
    name = models.CharField(max_length=50)
    minimum_hp = models.IntegerField(blank=True, null=True)
    maximum_hp = models.IntegerField(blank=True, null=True)
    minimum_ac = models.IntegerField(blank=True, null=True)
    maximum_ac = models.IntegerField(blank=True, null=True)
    minimum_fort = models.IntegerField(blank=True, null=True)
    maximum_fort = models.IntegerField(blank=True, null=True)
    minimum_ref = models.IntegerField(blank=True, null=True)
    maximum_ref = models.IntegerField(blank=True, null=True)
    minimum_will = models.IntegerField(blank=True, null=True)
    maximum_will = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    encounters = models.ManyToManyField(Encounter, through='CreatureInstance', related_name='creature_classes')

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

    def update_hp(self, new_min, new_max):
        if self.maximum_hp and new_max:
            if self.maximum_hp > new_max:
                self.maximum_hp = new_max
        elif new_max:
            self.maximum_hp = new_max
        if new_min and self.minimum_hp < new_min:
            self.minimum_hp = new_min
        self.save()

    def update_def(self, attribute, roll, is_hit):
        if attribute == _AC:
            if is_hit:
                if self.maximum_ac:
                    self.maximum_ac = min(self.maximum_ac, roll - 1)
                else:
                    self.maximum_ac = roll - 1
            else:
                self.minimum_ac = max(self.minimum_ac, roll)
        elif attribute == _FORT:
            if is_hit:
                if self.maximum_fort:
                    self.maximum_fort = min(self.maximum_fort, roll - 1)
                else:
                    self.maximum_fort = roll - 1
            else:
                self.minimum_fort = max(self.minimum_fort, roll)
        elif attribute == _REF:
            if is_hit:
                if self.maximum_ref:
                    self.maximum_ref = min(self.maximum_ref, roll - 1)
                else:
                    self.maximum_ref = roll - 1
            else:
                self.minimum_ref = max(self.minimum_ref, roll)
        elif attribute == _WILL:
            if is_hit:
                if self.maximum_will:
                    self.maximum_will = min(self.maximum_will, roll - 1)
                else:
                    self.maximum_will = roll - 1
            else:
                self.minimum_will = max(self.minimum_will, roll)
        self.save()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'creature class'
        verbose_name_plural = verbose_name + 'es'

class CreatureInstance(models.Model):
    creature_class = models.ForeignKey(CreatureClass, related_name='instances')
    encounter = models.ForeignKey(Encounter, related_name='creatures')
    encounter_label = models.CharField(max_length=50, default='unspecified')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def new_action(self, action):
        return self.actions.create(action)

    def name(self):
        return '%s - %s' % (self.encounter_label, self.creature_class.name)

    def damage_taken(self):
        return self.actions.filter(is_hit=True).aggregate(
            models.Sum('damage_roll'))['damage_roll__sum']

    def is_dead(self):
        return self.actions.filter(status_change=_DEAD).exists()

    def current_health(self):
        current_damage = self.damage_taken()
        if self.is_dead():
            return 'Dead'
        else:
            return _range(self.creature_class.minimum_hp - current_damage,
                          self.creature_class.maximum_hp - current_damage)

    def update_attributes(self):
        most_recent_action = self.actions.latest('created_at')
        if most_recent_action.is_hit:
            total_damage_taken = self.damage_taken()
            if most_recent_action.status_change == _BLOODIED:
                min_hp = total_damage_taken + 1
                max_hp = total_damage_taken * 2
                self.creature_class.update_hp(min_hp, max_hp)
            elif most_recent_action.status_change == _DEAD:
                min_hp = None
                max_hp = total_damage_taken
                self.creature_class.update_hp(min_hp, max_hp)
            elif most_recent_action.status_change == _NO_CHANGE:
                if self.actions.filter(status_change=_BLOODIED).exists():
                    min_hp = total_damage_taken + 1
                    max_hp = None
                    self.creature_class.update_hp(min_hp, max_hp)
                else:
                    min_hp = total_damage_taken * 2 + 1
                    max_hp = None
                    self.creature_class.update_hp(min_hp, max_hp)
        self.creature_class.update_def(most_recent_action.attack_vs,
                                       most_recent_action.attack_roll,
                                       most_recent_action.is_hit)

    def __unicode__(self):
        return self.name()

    class Meta:
        unique_together = ('encounter', 'encounter_label', 'creature_class')
        order_with_respect_to = 'encounter'
        ordering = ['-created_at', 'encounter_label']

class Action(models.Model):
    target = models.ForeignKey(CreatureInstance, related_name='actions')
    attack_roll = models.IntegerField()
    is_hit = models.BooleanField()
    attack_vs = models.IntegerField(choices=(
            (_AC, 'AC'),
            (_FORT, 'FORT'),
            (_REF, 'REF'),
            (_WILL, 'WILL'))
    )
    damage_roll = models.IntegerField(blank=True, null=True)
    status_change = models.IntegerField(choices=(
            (_NO_CHANGE, 'no change'),
            (_BLOODIED, 'became bloodied'),
            (_DEAD, 'became dead')),
        blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def encounter(self):
        return self.target.encounter

    def save(self):
        super(Action, self).save()
        self.target.update_attributes()

    def __unicode__(self):
        return '%s - %s' % (self.target, unicode(self.created_at))
