# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

class System(models.Model):
    name = models.CharField(_('name'), help_text=_('name-help'), max_length=100)
    description = models.CharField(_('description'), help_text=_('description-help'), max_length=200)
    external = models.BooleanField(_('Externo'))

    class Meta:
        verbose_name = _('system')
        verbose_name_plural = _('systems')
        
    def __unicode__(self):
        return self.name

class Module(models.Model):
    CRITICITY = (
        (u'H', _('high')),
        (u'M', _('medium')),
        (u'L', _('low')),
    )
    
    name = models.CharField(_('name'), help_text=_('name-help'), max_length=100)
    goal = models.CharField(_('goal'), help_text=_('goal-help'), max_length=200, blank=True)
    system = models.ForeignKey(System, verbose_name=_('system'), null=True, blank=True)
    external = models.BooleanField(_('external'))
    consumed = models.ManyToManyField('Interface', verbose_name = _('Interfaces Consumidas'), blank=True, related_name='consumers')
    criticity = models.CharField(_('criticity'), help_text=_('criticity-help'), max_length=2, choices=CRITICITY)

    class Meta:
        verbose_name = _('module')
        verbose_name_plural = _('modules')
        
    def __unicode__(self):
        return self.name

class Interface(models.Model):
    name = models.CharField(_('name'), help_text=_('name-help'), max_length=100)
    goal = models.CharField(_('goal'), help_text=_('goal-help'), max_length=200)
    technology = models.CharField(_('technology'), help_text=_('technology-help'), max_length=200)
    exposer = models.ForeignKey('Module', verbose_name = _('exposer'), related_name='exposed', null=True)

    class Meta:
        verbose_name = _('interface')
        verbose_name_plural = _('interfaces')
        
    def __unicode__(self):
        return self.name
