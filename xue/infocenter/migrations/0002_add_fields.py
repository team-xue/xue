# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'CentralStudentInfo.klass'
        db.add_column('infocenter_centralstudentinfo', 'klass', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['classes.LogicalClass'], null=True), keep_default=False)

        # Adding field 'CentralStudentInfo.join_date'
        db.add_column('infocenter_centralstudentinfo', 'join_date', self.gf('django.db.models.fields.DateField')(default=datetime.date(2012, 7, 2)), keep_default=False)

        # Adding field 'CentralStudentInfo.ethnic'
        db.add_column('infocenter_centralstudentinfo', 'ethnic', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'CentralStudentInfo.location'
        db.add_column('infocenter_centralstudentinfo', 'location', self.gf('django.db.models.fields.CharField')(default=u'', max_length=256), keep_default=False)

        # Adding field 'CentralStudentInfo.phone'
        db.add_column('infocenter_centralstudentinfo', 'phone', self.gf('django.db.models.fields.CharField')(default='', max_length=24, blank=True), keep_default=False)

        # Adding field 'CentralStudentInfo.political'
        db.add_column('infocenter_centralstudentinfo', 'political', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'CentralStudentInfo.nickname'
        db.add_column('infocenter_centralstudentinfo', 'nickname', self.gf('django.db.models.fields.CharField')(default=u'', max_length=32, blank=True), keep_default=False)

        # Adding field 'CentralStudentInfo.sign_line'
        db.add_column('infocenter_centralstudentinfo', 'sign_line', self.gf('django.db.models.fields.CharField')(default=u'', max_length=128, blank=True), keep_default=False)

        # Adding field 'CentralStudentInfo.high_school'
        db.add_column('infocenter_centralstudentinfo', 'high_school', self.gf('django.db.models.fields.CharField')(default=u'', max_length=32, blank=True), keep_default=False)

        # Adding field 'CentralStudentInfo.awards'
        db.add_column('infocenter_centralstudentinfo', 'awards', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'CentralStudentInfo.english_band_type'
        db.add_column('infocenter_centralstudentinfo', 'english_band_type', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True), keep_default=False)

        # Adding field 'CentralStudentInfo.english_band_score'
        db.add_column('infocenter_centralstudentinfo', 'english_band_score', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True), keep_default=False)

        # Adding field 'CentralStudentInfo.hobby'
        db.add_column('infocenter_centralstudentinfo', 'hobby', self.gf('django.db.models.fields.CharField')(default=u'', max_length=128, blank=True), keep_default=False)

        # Adding field 'CentralStudentInfo.health'
        db.add_column('infocenter_centralstudentinfo', 'health', self.gf('django.db.models.fields.CharField')(default=u'', max_length=64, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'CentralStudentInfo.klass'
        db.delete_column('infocenter_centralstudentinfo', 'klass_id')

        # Deleting field 'CentralStudentInfo.join_date'
        db.delete_column('infocenter_centralstudentinfo', 'join_date')

        # Deleting field 'CentralStudentInfo.ethnic'
        db.delete_column('infocenter_centralstudentinfo', 'ethnic')

        # Deleting field 'CentralStudentInfo.location'
        db.delete_column('infocenter_centralstudentinfo', 'location')

        # Deleting field 'CentralStudentInfo.phone'
        db.delete_column('infocenter_centralstudentinfo', 'phone')

        # Deleting field 'CentralStudentInfo.political'
        db.delete_column('infocenter_centralstudentinfo', 'political')

        # Deleting field 'CentralStudentInfo.nickname'
        db.delete_column('infocenter_centralstudentinfo', 'nickname')

        # Deleting field 'CentralStudentInfo.sign_line'
        db.delete_column('infocenter_centralstudentinfo', 'sign_line')

        # Deleting field 'CentralStudentInfo.high_school'
        db.delete_column('infocenter_centralstudentinfo', 'high_school')

        # Deleting field 'CentralStudentInfo.awards'
        db.delete_column('infocenter_centralstudentinfo', 'awards')

        # Deleting field 'CentralStudentInfo.english_band_type'
        db.delete_column('infocenter_centralstudentinfo', 'english_band_type')

        # Deleting field 'CentralStudentInfo.english_band_score'
        db.delete_column('infocenter_centralstudentinfo', 'english_band_score')

        # Deleting field 'CentralStudentInfo.hobby'
        db.delete_column('infocenter_centralstudentinfo', 'hobby')

        # Deleting field 'CentralStudentInfo.health'
        db.delete_column('infocenter_centralstudentinfo', 'health')


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
            'awards': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'english_band_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'english_band_type': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'ethnic': ('django.db.models.fields.IntegerField', [], {}),
            'health': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '64', 'blank': 'True'}),
            'high_school': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '32', 'blank': 'True'}),
            'hobby': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '128', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'join_date': ('django.db.models.fields.DateField', [], {}),
            'klass': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['classes.LogicalClass']", 'null': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'nickname': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '32', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '24', 'blank': 'True'}),
            'political': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sign_line': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '128', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'central_info'", 'unique': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['infocenter']
