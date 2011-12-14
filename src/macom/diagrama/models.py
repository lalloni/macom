# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import permalink
from django.forms.widgets import Textarea
from django.utils.translation import ugettext_lazy as _
from south.modelsinspector import add_introspection_rules
from taggit.managers import TaggableManager

# DEPRECADO: se deja por compatibilidad con migrations <= 0004
add_introspection_rules([], ["^diagrama\.models\.TextField60"])
add_introspection_rules([], ["^diagrama\.models\.TextField40"])

# DEPRECADO: se deja por compatibilidad con migrations <= 0004
class TextField60(models.TextField):
    # A more reasonably sized textarea                                                                                                            
    def formfield(self, **kwargs):
        kwargs.update(dict(widget=Textarea(attrs=dict(rows=7, cols=60))))
        return super(TextField60, self).formfield(**kwargs)

# DEPRECADO: se deja por compatibilidad con migrations <= 0004
class TextField40(models.TextField):
    # A more reasonably sized textarea                                                                                                            
    def formfield(self, **kwargs):
        kwargs.update(dict(widget=Textarea(attrs=dict(rows=7, cols=40))))
        return super(TextField40, self).formfield(**kwargs)

class Base(models.Model):
    class Meta:
        abstract = True
        db_tablespace = 'macom'
    @permalink
    def get_absolute_url(self):
        return ('%s_detail' % self._meta.module_name, [self.pk])

class Annotation(Base):
    annotation = models.TextField(_('annotation'))
    class Meta:
        abstract = True

class System(Base):
    name = models.CharField(_('name'), help_text=_('system-name-help'), max_length=100)
    description = models.TextField(_('description'), help_text=_('description-help'))
    functional_referents = models.TextField(_('functional_referents'), help_text=_('functional_referents-help'), blank=True)
    implementation_referents = models.TextField(_('implementation_referents'), help_text=_('implementation_referents-help'), blank=True)
    documentation = models.TextField(_('documentation'), help_text=_('documentation-help'), blank=True)
    external = models.BooleanField(_('external'), help_text=_('external-help'))
    tags = TaggableManager(blank=True)
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
    system = models.ForeignKey('System', verbose_name=_('system'), related_name='modules', null=True)
    name = models.CharField(_('name'), help_text=_('module-name-help'), max_length=100)
    goal = models.TextField(_('goal'), help_text=_('module-goal-help'))
    external = models.BooleanField(_('external'), help_text=_('external-help'))
    functional_referents = models.TextField(_('functional_referents'), help_text=_('functional_referents-help'), blank=True)
    implementation_referents = models.TextField(_('implementation_referents'), help_text=_('implementation_referents-help'), blank=True)
    documentation = models.TextField(_('documentation'), help_text=_('documentation-help'), blank=True)
    criticity = models.CharField(_('criticity'), help_text=_('criticity-help'), max_length=2, choices=CRITICITY)
    dependencies = models.ManyToManyField('Interface', through='Dependency', related_name='dependants')
    moduletypecases = models.ManyToManyField('ModuleType', through='ModuleTypeCase', related_name='moduletypecases')
    architecturalpatterncases = models.ManyToManyField('ArchitecturalPattern', through='ArchitecturalPatternCase', related_name='architecturalpatterncases')
    tags = TaggableManager(blank=True)
    class Meta:
        verbose_name = _('module')
        verbose_name_plural = _('modules')
        ordering = ['system__name']
    def __unicode__(self):
        return "%s:%s" % (unicode(self.system), self.name)
    def dependency_objects(self):
        return Dependency.objects.filter(module=self)

class Directionality:
    def direction(self, s_in='in', s_out='out', s_sep='-'):
        if self.direction_inbound and self.direction_outbound:
            return s_in + s_sep + s_out
        elif self.direction_inbound:
            return s_in
        elif self.direction_outbound:
            return s_out
        else:
            return ''

class Interface(Base, Directionality):
    module = models.ForeignKey(Module, related_name='interfaces', verbose_name=_('module'))
    name = models.CharField(_('name'), help_text=_('interface-name-help'), max_length=100)
    goal = models.TextField(_('goal'), help_text=_('interface-goal-help'))
    technology = models.CharField(_('technology'), help_text=_('technology-help') , max_length=200, blank=True)
    functional_referents = models.TextField(_('functional_referents'), help_text=_('functional_referents-help'), blank=True)
    implementation_referents = models.TextField(_('implementation_referents'), help_text=_('implementation_referents-help'), blank=True)
    documentation = models.TextField(_('documentation'), help_text=_('documentation-help'), blank=True)
    direction_inbound = models.BooleanField(_('Inbound'), help_text=_('interface-inbound-help'))
    direction_outbound = models.BooleanField(_('Outbound'), help_text=_('interface-outbound-help'))
    published = models.BooleanField(_('Published'), help_text=_('Published for use outside the system'))
    tags = TaggableManager(blank=True)
    class Meta:
        verbose_name = _('interface')
        verbose_name_plural = _('interfaces')
        ordering = ['module__system__name']
    def __unicode__(self):
        return "%s:%s" % (unicode(self.module), self.name)

class Dependency(Base, Directionality):
    module = models.ForeignKey(Module, verbose_name=_('module'))
    interface = models.ForeignKey(Interface, verbose_name=_('interface'))
    goal = models.TextField(_('goal'), help_text=_('dependency-goal-help') , blank=True)
    direction_inbound = models.BooleanField(_('Inbound'), help_text=_('dependency-inbound-help'))
    direction_outbound = models.BooleanField(_('Outbound'), help_text=_('dependency-outbound-help'))
    functional_referents = models.TextField(_('functional_referents'), help_text=_('functional_referents-help'), blank=True)
    implementation_referents = models.TextField(_('implementation_referents'), help_text=_('implementation_referents-help'), blank=True)
    documentation = models.TextField(_('documentation'), help_text=_('documentation-help') , blank=True)
    technology = models.CharField(_('technology'), help_text=_('technology-help') , max_length=200, blank=True)
    loadestimate = models.CharField(_('loadestimate'), help_text=_('loadestimate-help') , max_length=200, blank=True)
    class Meta:
        verbose_name = _('dependency')
        verbose_name_plural = _('dependencies')
        ordering = ['module__system__name']
    def __unicode__(self):
        return "%s:(%s)" % (unicode(self.module), unicode(self.interface))

class ArchitecturalPattern(Base):
    name = models.CharField(_('name'), help_text=_('architecturalpattern-name-help'), max_length=100)
    description = models.TextField(_('description'), help_text=_('architecturalpattern-description-help') , blank=True)
    tags = TaggableManager(blank=True)
    class Meta:
        verbose_name = _('architectural pattern')
        verbose_name_plural = _('architectural patterns')
        ordering = ['name']
    def __unicode__(self):
        return self.name

class ModuleType(Base):
    name = models.CharField(_('name'), help_text=_('moduletype-name-help'), max_length=100)
    description = models.TextField(_('description'), help_text=_('moduletype-description-help') , blank=True)
    class Meta:
        verbose_name = _('module type')
        verbose_name_plural = _('module types')
        ordering = ['name']
    def __unicode__(self):
        return self.name

class ArchitecturalPatternCase(Annotation):
    module = models.ForeignKey(Module)
    architecturalpattern = models.ForeignKey(ArchitecturalPattern, verbose_name=_('Architectural Pattern'), related_name='cases')
    class Meta:
        verbose_name = _('architectural pattern case')
        verbose_name_plural = _('architectural pattern cases')
        ordering = ['module__system__name']
    def __unicode__(self):
        return "%s:(%s)" % (unicode(self.module), unicode(self.architecturalpattern))

class ModuleTypeCase(Annotation):
    module = models.ForeignKey(Module)
    moduletype = models.ForeignKey(ModuleType, verbose_name=_('Module Type'))
    class Meta:
        verbose_name = _('module type case')
        verbose_name_plural = _('module type cases')
        ordering = ['module__system__name']
    def __unicode__(self):
        return "%s:(%s)" % (unicode(self.module), unicode(self.moduletype))
