# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'CentralStudentInfo.english_band_type'
        db.alter_column('infocenter_centralstudentinfo', 'english_band_type', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'CentralStudentInfo.english_band_score'
        db.alter_column('infocenter_centralstudentinfo', 'english_band_score', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'CentralStudentInfo.join_date'
        db.alter_column('infocenter_centralstudentinfo', 'join_date', self.gf('django.db.models.fields.DateField')(null=True))


    def backwards(self, orm):
        
        # Changing field 'CentralStudentInfo.english_band_type'
        db.alter_column('infocenter_centralstudentinfo', 'english_band_type', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'CentralStudentInfo.english_band_score'
        db.alter_column('infocenter_centralstudentinfo', 'english_band_score', self.gf('django.db.models.fields.IntegerField')())

        # User chose to not deal with backwards NULL issues for 'CentralStudentInfo.join_date'
        raise RuntimeError("Cannot reverse this migration. 'CentralStudentInfo.join_date' and its values cannot be restored.")


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
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
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'infocenter.centralstudentinfo': {
            'Meta': {'object_name': 'CentralStudentInfo'},
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'cpc_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'cylc_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'english_band_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'english_band_type': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'ethnic': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'health': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '64', 'blank': 'True'}),
            'high_school': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '32', 'blank': 'True'}),
            'hobby': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '128', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'ident_ma': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'ident_pa': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'is_locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'join_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'klass': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['classes.LogicalClass']", 'null': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'name_ma': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'name_pa': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '24', 'blank': 'True'}),
            'phone_family': ('django.db.models.fields.CharField', [], {'max_length': '24', 'blank': 'True'}),
            'political': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'postal': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'railway_station': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'unit_ma': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'unit_pa': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'central_info'", 'unique': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['infocenter']
