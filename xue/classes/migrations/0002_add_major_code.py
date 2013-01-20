# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Major.code'
        db.add_column('classes_major', 'code', self.gf('django.db.models.fields.CharField')(default=u'', max_length=4), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Major.code'
        db.delete_column('classes_major', 'code')


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
            'code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        }
    }

    complete_apps = ['classes']
