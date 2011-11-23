# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'System.functional_referents'
        db.add_column('diagrama_system', 'functional_referents', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'System.implementation_referents'
        db.add_column('diagrama_system', 'implementation_referents', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'Interface.functional_referents'
        db.add_column('diagrama_interface', 'functional_referents', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'Interface.implementation_referents'
        db.add_column('diagrama_interface', 'implementation_referents', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'Dependency.functional_referents'
        db.add_column('diagrama_dependency', 'functional_referents', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'Dependency.implementation_referents'
        db.add_column('diagrama_dependency', 'implementation_referents', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'Module.functional_referents'
        db.add_column('diagrama_module', 'functional_referents', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'Module.implementation_referents'
        db.add_column('diagrama_module', 'implementation_referents', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'System.functional_referents'
        db.delete_column('diagrama_system', 'functional_referents')

        # Deleting field 'System.implementation_referents'
        db.delete_column('diagrama_system', 'implementation_referents')

        # Deleting field 'Interface.functional_referents'
        db.delete_column('diagrama_interface', 'functional_referents')

        # Deleting field 'Interface.implementation_referents'
        db.delete_column('diagrama_interface', 'implementation_referents')

        # Deleting field 'Dependency.functional_referents'
        db.delete_column('diagrama_dependency', 'functional_referents')

        # Deleting field 'Dependency.implementation_referents'
        db.delete_column('diagrama_dependency', 'implementation_referents')

        # Deleting field 'Module.functional_referents'
        db.delete_column('diagrama_module', 'functional_referents')

        # Deleting field 'Module.implementation_referents'
        db.delete_column('diagrama_module', 'implementation_referents')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'diagrama.architecturalpattern': {
            'Meta': {'ordering': "['name']", 'object_name': 'ArchitecturalPattern'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'diagrama.architecturalpatterncase': {
            'Meta': {'ordering': "['module__system__name']", 'object_name': 'ArchitecturalPatternCase'},
            'annotation': ('django.db.models.fields.TextField', [], {}),
            'architecturalpattern': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['diagrama.ArchitecturalPattern']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['diagrama.Module']"})
        },
        'diagrama.dependency': {
            'Meta': {'ordering': "['module__system__name']", 'object_name': 'Dependency'},
            'direction_inbound': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'direction_outbound': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'documentation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'functional_referents': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'goal': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'implementation_referents': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'interface': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['diagrama.Interface']"}),
            'loadestimate': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['diagrama.Module']"}),
            'referents': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'technology': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'diagrama.interface': {
            'Meta': {'ordering': "['module__system__name']", 'object_name': 'Interface'},
            'direction_inbound': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'direction_outbound': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'documentation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'functional_referents': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'goal': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'implementation_referents': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interfaces'", 'to': "orm['diagrama.Module']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'referents': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'technology': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'diagrama.module': {
            'Meta': {'ordering': "['system__name']", 'object_name': 'Module'},
            'architecturalpatterncases': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'architecturalpatterncases'", 'symmetrical': 'False', 'through': "orm['diagrama.ArchitecturalPatternCase']", 'to': "orm['diagrama.ArchitecturalPattern']"}),
            'criticity': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'dependencies': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'dependants'", 'symmetrical': 'False', 'through': "orm['diagrama.Dependency']", 'to': "orm['diagrama.Interface']"}),
            'documentation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'external': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'functional_referents': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'goal': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'implementation_referents': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'moduletypecases': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'moduletypecases'", 'symmetrical': 'False', 'through': "orm['diagrama.ModuleTypeCase']", 'to': "orm['diagrama.ModuleType']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'referents': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'modules'", 'null': 'True', 'to': "orm['diagrama.System']"})
        },
        'diagrama.moduletype': {
            'Meta': {'ordering': "['name']", 'object_name': 'ModuleType'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'diagrama.moduletypecase': {
            'Meta': {'ordering': "['module__system__name']", 'object_name': 'ModuleTypeCase'},
            'annotation': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['diagrama.Module']"}),
            'moduletype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['diagrama.ModuleType']"})
        },
        'diagrama.system': {
            'Meta': {'ordering': "['name']", 'object_name': 'System'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'documentation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'external': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'functional_referents': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'implementation_referents': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'referents': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['diagrama']
