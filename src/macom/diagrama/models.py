# -*- coding: utf-8 -*-

from django.db import models

class System(models.Model):
    name = models.CharField(u'Nombre', max_length=100)
    description = models.TextField(u'Derscripción')

    class Meta:
        verbose_name = 'Sistema'
        verbose_name_plural = 'Sistemas'
        
    def __unicode__(self):
        return self.name

class Module(models.Model):
    name = models.CharField(u'Nombre', max_length=100)
    goal = models.TextField(u'Objetivo')
    system = models.ForeignKey(System, verbose_name=u'Sistema')
    external = models.BooleanField(u'Externo')

    class Meta:
        verbose_name = 'Modulo'
        verbose_name_plural = 'Modulos'
        
    def __unicode__(self):
        return self.name

class Interface(models.Model):
    CRITICITY = (
        (u'H', 'Alta'),
        (u'M', 'Media'),
        (u'L', 'Baja'),
    )

    name = models.CharField(u'Nombre', max_length=100)
    goal = models.CharField(u'Objetivo', max_length=200)
    technology = models.CharField(u'Tecnología', max_length=200)
    volume = models.CharField(u'Volumen', max_length=100)
    module = models.ForeignKey(Module, verbose_name=u'Módulo')
    criticity = models.CharField(u'Criticidad', max_length=2, choices=CRITICITY)

    def __unicode__(self):
        return self.name

class ExposedInterface(Interface):
    clients = models.ManyToManyField(Module, verbose_name = 'Clientes')

class ConsumedInterface(Interface):
    contrapart = models.OneToOneField(Module, verbose_name = 'Contraparte')
