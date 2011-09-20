# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Module.goal'
        db.alter_column('diagrama_module', 'goal', self.gf('diagrama.models.MyTextField')())

        # Changing field 'Module.referents'
        db.alter_column('diagrama_module', 'referents', self.gf('diagrama.models.MyTextField')())

        # Changing field 'Module.documentation'
        db.alter_column('diagrama_module', 'documentation', self.gf('diagrama.models.MyTextField')())

        # Changing field 'System.description'
        db.alter_column('diagrama_system', 'description', self.gf('diagrama.models.MyTextField')())

        # Changing field 'System.referents'
        db.alter_column('diagrama_system', 'referents', self.gf('diagrama.models.MyTextField')())

        # Adding field 'Interface.direction_inbound'
        db.add_column('diagrama_interface', 'direction_inbound', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Interface.direction_outbound'
        db.add_column('diagrama_interface', 'direction_outbound', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Changing field 'Interface.goal'
        db.alter_column('diagrama_interface', 'goal', self.gf('diagrama.models.MyTextField')())

        # Changing field 'Interface.documentation'
        db.alter_column('diagrama_interface', 'documentation', self.gf('diagrama.models.MyTextField')())

        # Changing field 'Interface.referents'
        db.alter_column('diagrama_interface', 'referents', self.gf('diagrama.models.MyTextField')())

        # Changing field 'Interface.technology'
        db.alter_column('diagrama_interface', 'technology', self.gf('diagrama.models.MyTextField')())


    def backwards(self, orm):
        
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

        # Deleting field 'Interface.direction_inbound'
        db.delete_column('diagrama_interface', 'direction_inbound')

        # Deleting field 'Interface.direction_outbound'
        db.delete_column('diagrama_interface', 'direction_outbound')

        # Changing field 'Interface.goal'
        db.alter_column('diagrama_interface', 'goal', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Interface.documentation'
        db.alter_column('diagrama_interface', 'documentation', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Interface.referents'
        db.alter_column('diagrama_interface', 'referents', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Interface.technology'
        db.alter_column('diagrama_interface', 'technology', self.gf('django.db.models.fields.TextField')())


    models = {
        'diagrama.interface': {
            'Meta': {'ordering': "['exposer__name']", 'object_name': 'Interface'},
            'direction_inbound': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'direction_outbound': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'documentation': ('diagrama.models.MyTextField', [], {'blank': 'True'}),
            'exposer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'exposed'", 'null': 'True', 'to': "orm['diagrama.Module']"}),
            'goal': ('diagrama.models.MyTextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'referents': ('diagrama.models.MyTextField', [], {'blank': 'True'}),
            'technology': ('diagrama.models.MyTextField', [], {})
        },
        'diagrama.module': {
            'Meta': {'ordering': "['system__name']", 'object_name': 'Module'},
            'consumed': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'consumers'", 'blank': 'True', 'to': "orm['diagrama.Interface']"}),
            'criticity': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'documentation': ('diagrama.models.MyTextField', [], {'blank': 'True'}),
            'external': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'goal': ('diagrama.models.MyTextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'referents': ('diagrama.models.MyTextField', [], {'blank': 'True'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['diagrama.System']", 'null': 'True', 'blank': 'True'})
        },
        'diagrama.system': {
            'Meta': {'ordering': "['name']", 'object_name': 'System'},
            'description': ('diagrama.models.MyTextField', [], {}),
            'documentation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'external': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'referents': ('diagrama.models.MyTextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['diagrama']
