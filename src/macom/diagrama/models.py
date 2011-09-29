# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.forms import Textarea
from south.modelsinspector import add_introspection_rules

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
    name = models.CharField(_('name'), help_text=_('system-name-help'), max_length=100)
    description = models.TextField(_('description'), help_text=_('description-help'))
    referents = models.TextField(_('referents'), help_text=_('referents-help'), blank=True)
    documentation = models.TextField(_('documentation'), help_text=_('documentation-help'), blank=True)
    external = models.BooleanField(_('external'), help_text=_('external-help'))

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
    
    system = models.ForeignKey(System, verbose_name=_('system'), null=True)
    
    name = models.CharField(_('name'), help_text=_('module-name-help'), max_length=100)
    goal = models.TextField(_('goal'), help_text=_('module-goal-help'))
    
    external = models.BooleanField(_('external'), help_text=_('external-help'))
    referents = models.TextField(_('referents'), help_text=_('referents-help'), blank=True)
    documentation = models.TextField(_('documentation'), help_text=_('documentation-help'), blank=True)
    criticity = models.CharField(_('criticity'), help_text=_('criticity-help'), max_length=2, choices=CRITICITY)

    dependencies = models.ManyToManyField('Interface', through='Dependency', related_name='dependencies')

    class Meta:
        verbose_name = _('module')
        verbose_name_plural = _('modules')
        ordering = ['system__name']

    def __unicode__(self):
        return "%s:%s" % (unicode(self.system), self.name)

class Interface(Base):
    name = models.CharField(_('name'), help_text=_('interface-name-help'), max_length=100)
    goal = models.TextField(_('goal'), help_text=_('interface-goal-help') )
    technology = models.TextField(_('technology'), help_text=_('technology-help'))
    referents = models.TextField(_('referents'), help_text=_('referents-help'), blank=True)
    documentation = models.TextField(_('documentation'), help_text=_('documentation-help'), blank=True)
    direction_inbound = models.BooleanField(_('Inbound'), help_text=_('interface-inbound-help'))
    direction_outbound = models.BooleanField(_('Outbound'), help_text=_('interface-outbound-help'))
    exposer = models.ForeignKey('Module', verbose_name = _('exposer'), related_name='exposed', null=True)

    class Meta:
        verbose_name = _('interface')
        verbose_name_plural = _('interfaces')
        ordering = ['exposer__system__name']

    def __unicode__(self):
        return "%s:%s" % (unicode(self.exposer), self.name)

class Dependency(Base):
    exposer = models.ForeignKey('Module', verbose_name = _('exposer'), related_name='dependency', null=True)
    interface = models.ForeignKey(Interface)
    goal = models.TextField(_('goal'), help_text=_('dependency-goal-help') , blank=True)
    direction_inbound = models.BooleanField(_('Inbound'), help_text=_('dependency-inbound-help'))
    direction_outbound = models.BooleanField(_('Outbound'), help_text=_('dependency-outbound-help'))
    referents = models.TextField(_('referents'), help_text=_('referents-help') , blank=True)
    documentation = models.TextField(_('documentation'), help_text=_('documentation-help') , blank=True)
    technology = models.CharField(_('technology'), help_text=_('technology-help') , max_length=200, blank=True)
    loadestimate = models.CharField(_('loadestimate'), help_text=_('loadestimate-help') , max_length=200, blank=True)

    class Meta:
        verbose_name = _('dependency')
        verbose_name_plural = _('dependencies')
        ordering = ['exposer__system__name']

    def __unicode__(self):
        return "%s (%s)" % (unicode(self.exposer), self.interface)
