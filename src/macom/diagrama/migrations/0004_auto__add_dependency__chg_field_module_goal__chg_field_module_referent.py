# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Dependency'
        db.create_table('diagrama_dependency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exposer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dependency', null=True, to=orm['diagrama.Module'])),
            ('interface', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['diagrama.Interface'])),
            ('goal', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('direction_inbound', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('direction_outbound', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('referents', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('documentation', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('technology', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('loadestimate', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('diagrama', ['Dependency'])

        # Changing field 'Module.goal'
        db.alter_column('diagrama_module', 'goal', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Module.referents'
        db.alter_column('diagrama_module', 'referents', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Module.documentation'
        db.alter_column('diagrama_module', 'documentation', self.gf('django.db.models.fields.TextField')())

        # Changing field 'System.description'
        db.alter_column('diagrama_system', 'description', self.gf('django.db.models.fields.TextField')())

        # Changing field 'System.referents'
        db.alter_column('diagrama_system', 'referents', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Interface.goal'
        db.alter_column('diagrama_interface', 'goal', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Interface.referents'
        db.alter_column('diagrama_interface', 'referents', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Interface.documentation'
        db.alter_column('diagrama_interface', 'documentation', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Interface.technology'
        db.alter_column('diagrama_interface', 'technology', self.gf('django.db.models.fields.TextField')())


    def backwards(self, orm):
        
        # Deleting model 'Dependency'
        db.delete_table('diagrama_dependency')

        # Changing field 'Module.goal'
        db.alter_column('diagrama_module', 'goal', self.gf('diagrama.models.TextField60')())

        # Changing field 'Module.referents'
        db.alter_column('diagrama_module', 'referents', self.gf('diagrama.models.TextField60')())

        # Changing field 'Module.documentation'
        db.alter_column('diagrama_module', 'documentation', self.gf('diagrama.models.TextField60')())

        # Changing field 'System.description'
        db.alter_column('diagrama_system', 'description', self.gf('diagrama.models.TextField60')())

        # Changing field 'System.referents'
        db.alter_column('diagrama_system', 'referents', self.gf('diagrama.models.TextField60')())

        # Changing field 'Interface.goal'
        db.alter_column('diagrama_interface', 'goal', self.gf('diagrama.models.TextField40')())

        # Changing field 'Interface.referents'
        db.alter_column('diagrama_interface', 'referents', self.gf('diagrama.models.TextField40')())

        # Changing field 'Interface.documentation'
        db.alter_column('diagrama_interface', 'documentation', self.gf('diagrama.models.TextField60')())

        # Changing field 'Interface.technology'
        db.alter_column('diagrama_interface', 'technology', self.gf('diagrama.models.TextField40')())


    models = {
        'diagrama.dependency': {
            'Meta': {'ordering': "['exposer__system__name']", 'object_name': 'Dependency'},
            'direction_inbound': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'direction_outbound': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'documentation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'exposer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dependency'", 'null': 'True', 'to': "orm['diagrama.Module']"}),
            'goal': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interface': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['diagrama.Interface']"}),
            'loadestimate': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'referents': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'technology': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'diagrama.interface': {
            'Meta': {'ordering': "['exposer__system__name']", 'object_name': 'Interface'},
            'direction_inbound': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'direction_outbound': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'documentation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'exposer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'exposed'", 'null': 'True', 'to': "orm['diagrama.Module']"}),
            'goal': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'referents': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'technology': ('django.db.models.fields.TextField', [], {})
        },
        'diagrama.module': {
            'Meta': {'ordering': "['system__name']", 'object_name': 'Module'},
            'consumed': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'consumers'", 'blank': 'True', 'to': "orm['diagrama.Interface']"}),
            'criticity': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'dependencies': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'dependencies'", 'symmetrical': 'False', 'through': "orm['diagrama.Dependency']", 'to': "orm['diagrama.Interface']"}),
            'documentation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'external': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'goal': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'referents': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['diagrama.System']", 'null': 'True'})
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
