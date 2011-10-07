# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        for d in orm.Dependency.objects.all():
            d.module_id = d.exposer.pk
            d.save()
        for d in orm.Interface.objects.all():
            d.module = d.exposer
            d.save()

    def backwards(self, orm):
        for d in orm.Dependency.objects.all():
            d.exposer = orm.Module.objects.get(d.module_id)
            d.save()
        for d in orm.Interface.objects.all():
            d.exposer = d.module
            d.save()

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
            'module_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
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
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['diagrama.Module']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'referents': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'technology': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        'diagrama.module': {
            'Meta': {'ordering': "['system__name']", 'object_name': 'Module'},
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
