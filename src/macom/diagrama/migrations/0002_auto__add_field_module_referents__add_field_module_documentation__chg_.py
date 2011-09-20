# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Module.referents'
        db.add_column('diagrama_module', 'referents', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'Module.documentation'
        db.add_column('diagrama_module', 'documentation', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Changing field 'Module.goal'
        db.alter_column('diagrama_module', 'goal', self.gf('django.db.models.fields.TextField')())

        # Adding field 'System.referents'
        db.add_column('diagrama_system', 'referents', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'System.documentation'
        db.add_column('diagrama_system', 'documentation', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Changing field 'System.description'
        db.alter_column('diagrama_system', 'description', self.gf('django.db.models.fields.TextField')())

        # Adding field 'Interface.referents'
        db.add_column('diagrama_interface', 'referents', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'Interface.documentation'
        db.add_column('diagrama_interface', 'documentation', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Changing field 'Interface.technology'
        db.alter_column('diagrama_interface', 'technology', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Interface.goal'
        db.alter_column('diagrama_interface', 'goal', self.gf('django.db.models.fields.TextField')())


    def backwards(self, orm):
        
        # Deleting field 'Module.referents'
        db.delete_column('diagrama_module', 'referents')

        # Deleting field 'Module.documentation'
        db.delete_column('diagrama_module', 'documentation')

        # Changing field 'Module.goal'
        db.alter_column('diagrama_module', 'goal', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Deleting field 'System.referents'
        db.delete_column('diagrama_system', 'referents')

        # Deleting field 'System.documentation'
        db.delete_column('diagrama_system', 'documentation')

        # Changing field 'System.description'
        db.alter_column('diagrama_system', 'description', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Deleting field 'Interface.referents'
        db.delete_column('diagrama_interface', 'referents')

        # Deleting field 'Interface.documentation'
        db.delete_column('diagrama_interface', 'documentation')

        # Changing field 'Interface.technology'
        db.alter_column('diagrama_interface', 'technology', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Interface.goal'
        db.alter_column('diagrama_interface', 'goal', self.gf('django.db.models.fields.CharField')(max_length=200))


    models = {
        'diagrama.interface': {
            'Meta': {'ordering': "['exposer__name']", 'object_name': 'Interface'},
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
            'documentation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'external': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'goal': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'referents': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['diagrama.System']", 'null': 'True', 'blank': 'True'})
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
