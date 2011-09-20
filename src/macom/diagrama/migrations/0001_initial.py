# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'System'
        db.create_table('diagrama_system', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('external', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('diagrama', ['System'])

        # Adding model 'Module'
        db.create_table('diagrama_module', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('goal', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('system', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['diagrama.System'], null=True, blank=True)),
            ('external', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('criticity', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('diagrama', ['Module'])

        # Adding M2M table for field consumed on 'Module'
        db.create_table('diagrama_module_consumed', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('module', models.ForeignKey(orm['diagrama.module'], null=False)),
            ('interface', models.ForeignKey(orm['diagrama.interface'], null=False))
        ))
        db.create_unique('diagrama_module_consumed', ['module_id', 'interface_id'])

        # Adding model 'Interface'
        db.create_table('diagrama_interface', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('goal', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('technology', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('exposer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='exposed', null=True, to=orm['diagrama.Module'])),
        ))
        db.send_create_signal('diagrama', ['Interface'])


    def backwards(self, orm):
        
        # Deleting model 'System'
        db.delete_table('diagrama_system')

        # Deleting model 'Module'
        db.delete_table('diagrama_module')

        # Removing M2M table for field consumed on 'Module'
        db.delete_table('diagrama_module_consumed')

        # Deleting model 'Interface'
        db.delete_table('diagrama_interface')


    models = {
        'diagrama.interface': {
            'Meta': {'ordering': "['exposer']", 'object_name': 'Interface'},
            'exposer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'exposed'", 'null': 'True', 'to': "orm['diagrama.Module']"}),
            'goal': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'technology': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'diagrama.module': {
            'Meta': {'ordering': "['name']", 'object_name': 'Module'},
            'consumed': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'consumers'", 'blank': 'True', 'to': "orm['diagrama.Interface']"}),
            'criticity': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'external': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'goal': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['diagrama.System']", 'null': 'True', 'blank': 'True'})
        },
        'diagrama.system': {
            'Meta': {'ordering': "['name']", 'object_name': 'System'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'external': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['diagrama']
