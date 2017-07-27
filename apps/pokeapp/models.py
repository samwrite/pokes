# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..loginapp .models import User

# Create your models here.    
class PokeManager(models.Manager):
    def createPoke(self, poker, poked):
        if Poke.objects.filter(poker=poker, poked=poked):
            existing = Poke.objects.get(poker=poker, poked=poked)
            existing.counter += 1
            existing.save()
        else:
            Poke.objects.create(
                poker = poker,
                poked = poked,
            )

class Poke(models.Model):
    poker = models.ForeignKey(User, related_name="pokerpokes")
    poked = models.ForeignKey(User, related_name="pokedpokes")
    counter = models.IntegerField(blank=False, default=1, null=True)
    objects = PokeManager()