# -*- coding: utf-8 -*-

from django.db import models

class Poll(models.Model):
    question = models.CharField('pregunta', max_length=200)
    pub_date = models.DateTimeField('fecha de publicación')
    
    def __unicode__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField('opción', max_length=200)
    votes = models.IntegerField('votos')
    
    def __unicode__(self):
        return self.choice
