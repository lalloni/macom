# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.forms import Textarea
from south.modelsinspector import add_introspection_rules

# Agrega instrospeccion para que la migracion funcione con Custom Fields simples
add_introspection_rules([], ["^diagrama\.models\.TextField60"])
add_introspection_rules([], ["^diagrama\.models\.TextField40"])

class TextField60(models.TextField):
#A more reasonably sized textarea                                                                                                            
    def formfield(self, **kwargs):
        kwargs.update(
            {"widget": Textarea(attrs={'rows':7, 'cols':60})}
        )
        return super(TextField60, self).formfield(**kwargs)

class TextField40(models.TextField):
#A more reasonably sized textarea                                                                                                            
    def formfield(self, **kwargs):
        kwargs.update(
            {"widget": Textarea(attrs={'rows':7, 'cols':40})}
        )
        return super(TextField40, self).formfield(**kwargs)


class Base(models.Model):
    @permalink
    def get_absolute_url(self):
        return ('admin:%s_%s_change' %(self._meta.app_label, self._meta.module_name), [self.id])

    class Meta:
        abstract = True

class System(Base):
    name = models.CharField(_('name'), help_text=_('name-help'), max_length=100)
    description = TextField60(_('description'), help_text=_('description-help'))
    referents = TextField60(_('referents'), help_text=_('referents-help'), blank=True)
    documentation = models.TextField(_('documentation'), help_text=_('documentation-help'), blank=True)
    external = models.BooleanField(_('Externo'))

    class Meta:
        verbose_name = _('system')
        verbose_name_plural = _('systems')
        ordering = ['name']
        
    def __unicode__(self):
        return self.name

class Module(Base):
    CRITICITY = (
        (u'H', _('high')),
        (u'M', _('medium')),
        (u'L', _('low')),
    )
    
    name = models.CharField(_('name'), help_text=_('name-help'), max_length=100)
    goal = TextField60(_('goal'), help_text=_('goal-help'))
    system = models.ForeignKey(System, verbose_name=_('system'), null=True)
    external = models.BooleanField(_('external'))
    consumed = models.ManyToManyField('Interface', verbose_name = _('Interfaces Consumidas'), blank=True, related_name='consumers')
    referents = TextField60(_('referents'), help_text=_('referents-help'), blank=True)
    documentation = TextField60(_('documentation'), help_text=_('documentation-help'), blank=True)
    criticity = models.CharField(_('criticity'), help_text=_('criticity-help'), max_length=2, choices=CRITICITY)

    class Meta:
        verbose_name = _('module')
        verbose_name_plural = _('modules')
        ordering = ['system__name']

    def __unicode__(self):
        return "%s:%s" % (unicode(self.system), self.name)

class Interface(Base):
    name = models.CharField(_('name'), help_text=_('name-help'), max_length=100)
    goal = TextField40(_('goal'), help_text=_('goal-help') )
    technology = TextField40(_('technology'), help_text=_('technology-help'))
    referents = TextField40(_('referents'), help_text=_('referents-help'), blank=True)
    documentation = TextField60(_('documentation'), help_text=_('documentation-help'), blank=True)
    direction_inbound = models.BooleanField(_('Inbound'))
    direction_outbound = models.BooleanField(_('Outbound'))
    exposer = models.ForeignKey('Module', verbose_name = _('exposer'), related_name='exposed', null=True)

    class Meta:
        verbose_name = _('interface')
        verbose_name_plural = _('interfaces')
        ordering = ['exposer__name']

    def __unicode__(self):
        return "%s:%s" % (unicode(self.exposer), self.name)