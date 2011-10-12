# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ArchitecturalPatternCase'
        db.create_table('diagrama_architecturalpatterncase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('annotation', self.gf('django.db.models.fields.TextField')()),
            ('module', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['diagrama.Module'])),
            ('architecturalpattern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['diagrama.ArchitecturalPattern'])),
        ))
        db.send_create_signal('diagrama', ['ArchitecturalPatternCase'])

        # Adding model 'ArchitecturalPattern'
        db.create_table('diagrama_architecturalpattern', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('diagrama', ['ArchitecturalPattern'])

        # Adding model 'ModuleType'
        db.create_table('diagrama_moduletype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('diagrama', ['ModuleType'])

        # Adding model 'ModuleTypeCase'
        db.create_table('diagrama_moduletypecase', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('annotation', self.gf('django.db.models.fields.TextField')()),
            ('module', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['diagrama.Module'])),
            ('moduletype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['diagrama.ModuleType'])),
        ))
        db.send_create_signal('diagrama', ['ModuleTypeCase'])


    def backwards(self, orm):
        
        # Deleting model 'ArchitecturalPatternCase'
        db.delete_table('diagrama_architecturalpatterncase')

        # Deleting model 'ArchitecturalPattern'
        db.delete_table('diagrama_architecturalpattern')

        # Deleting model 'ModuleType'
        db.delete_table('diagrama_moduletype')

        # Deleting model 'ModuleTypeCase'
        db.delete_table('diagrama_moduletypecase')


    models = {
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
            'goal': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'goal': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interfaces'", 'to': "orm['diagrama.Module']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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
            'goal': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'referents': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['diagrama']
