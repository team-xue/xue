# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Major'
        db.create_table('classes_major', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('shortname', self.gf('django.db.models.fields.CharField')(max_length=4)),
        ))
        db.send_create_signal('classes', ['Major'])

        # Adding model 'LogicalClass'
        db.create_table('classes_logicalclass', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('seq', self.gf('django.db.models.fields.IntegerField')()),
            ('major', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['classes.Major'])),
        ))
        db.send_create_signal('classes', ['LogicalClass'])


    def backwards(self, orm):
        
        # Deleting model 'Major'
        db.delete_table('classes_major')

        # Deleting model 'LogicalClass'
        db.delete_table('classes_logicalclass')


    models = {
        'classes.logicalclass': {
            'Meta': {'object_name': 'LogicalClass'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'major': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['classes.Major']"}),
            'seq': ('django.db.models.fields.IntegerField', [], {})
        },
        'classes.major': {
            'Meta': {'object_name': 'Major'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        }
    }

    complete_apps = ['classes']
