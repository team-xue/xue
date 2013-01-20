# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ApplicationEntry'
        db.create_table('springaid2012_applicationentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('ctime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('poverty_status', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('is_applied_loan', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('scholarship_lvl', self.gf('django.db.models.fields.IntegerField')()),
            ('overall_rank', self.gf('django.db.models.fields.IntegerField')()),
            ('aid_apply_for', self.gf('django.db.models.fields.IntegerField')()),
            ('cee_score_pastline', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('english_band', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('home_addr', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('application_text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('springaid2012', ['ApplicationEntry'])


    def backwards(self, orm):
        
        # Deleting model 'ApplicationEntry'
        db.delete_table('springaid2012_applicationentry')


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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'springaid2012.applicationentry': {
            'Meta': {'object_name': 'ApplicationEntry'},
            'aid_apply_for': ('django.db.models.fields.IntegerField', [], {}),
            'application_text': ('django.db.models.fields.TextField', [], {}),
            'cee_score_pastline': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'ctime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'english_band': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'home_addr': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_applied_loan': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'overall_rank': ('django.db.models.fields.IntegerField', [], {}),
            'poverty_status': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'scholarship_lvl': ('django.db.models.fields.IntegerField', [], {}),
            'student': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['springaid2012']
