# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

class System(models.Model):
    name = models.CharField(_('name'), max_length=100)
    description = models.CharField(_('description'), max_length=200)

    class Meta:
        verbose_name = _('system')
        verbose_name_plural = _('systems')
        
    def __unicode__(self):
        return self.name

class Module(models.Model):
    name = models.CharField(_('name'), max_length=100)
    goal = models.CharField(_('goal'), max_length=200)
    system = models.ForeignKey(System, verbose_name=_('system'))
    external = models.BooleanField(_('external'))

    class Meta:
        verbose_name = _('module')
        verbose_name_plural = _('modules')
        
    def __unicode__(self):
        return self.name

class Interface(models.Model):
    CRITICITY = (
        (u'H', _('high')),
        (u'M', _('medium')),
        (u'L', _('low')),
    )

    name = models.CharField(_('name'), max_length=100)
    goal = models.CharField(_('goal'), max_length=200)
    technology = models.CharField(_('technology'), max_length=200)
    volume = models.CharField(_('volume'), max_length=100)
    module = models.ForeignKey(Module, verbose_name=_('module'))
    criticity = models.CharField(_('criticity'), max_length=2, choices=CRITICITY)

    def __unicode__(self):
        return self.name

class ExposedInterface(Interface):
    clients = models.ManyToManyField(Module, verbose_name = 'Clientes')
    
    class Meta:
        verbose_name = _('exposed-interface')
        verbose_name_plural = _('exposed-interfaces')

class ConsumedInterface(Interface):
    contrapart = models.OneToOneField(Module, verbose_name = 'Contraparte')
    
    class Meta:
        verbose_name = _('consumed-interface')
        verbose_name_plural = _('consumed-interfaces')
