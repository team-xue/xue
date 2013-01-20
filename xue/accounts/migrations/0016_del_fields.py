# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'DMUserProfile.english_band_type'
        db.delete_column('accounts_dmuserprofile', 'english_band_type')

        # Deleting field 'DMUserProfile.political'
        db.delete_column('accounts_dmuserprofile', 'political')

        # Deleting field 'DMUserProfile.health'
        db.delete_column('accounts_dmuserprofile', 'health')

        # Deleting field 'DMUserProfile.location'
        db.delete_column('accounts_dmuserprofile', 'location')

        # Deleting field 'DMUserProfile.english_band_score'
        db.delete_column('accounts_dmuserprofile', 'english_band_score')

        # Deleting field 'DMUserProfile.hobby'
        db.delete_column('accounts_dmuserprofile', 'hobby')

        # Deleting field 'DMUserProfile.high_school'
        db.delete_column('accounts_dmuserprofile', 'high_school')

        # Deleting field 'DMUserProfile.phone'
        db.delete_column('accounts_dmuserprofile', 'phone')

        # Deleting field 'DMUserProfile.awards'
        db.delete_column('accounts_dmuserprofile', 'awards')

        # Deleting field 'DMUserProfile.ethnic'
        db.delete_column('accounts_dmuserprofile', 'ethnic')

        # Deleting field 'DMUserProfile.nickname'
        db.delete_column('accounts_dmuserprofile', 'nickname')

        # Deleting field 'DMUserProfile.sign_line'
        db.delete_column('accounts_dmuserprofile', 'sign_line')

        # Deleting field 'DMUserProfile.join_date'
        db.delete_column('accounts_dmuserprofile', 'join_date')

        # Deleting field 'DMUserProfile.klass'
        db.delete_column('accounts_dmuserprofile', 'klass_id')


    def backwards(self, orm):
        
        # Adding field 'DMUserProfile.english_band_type'
        db.add_column('accounts_dmuserprofile', 'english_band_type', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True), keep_default=False)

        # Adding field 'DMUserProfile.political'
        db.add_column('accounts_dmuserprofile', 'political', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'DMUserProfile.health'
        db.add_column('accounts_dmuserprofile', 'health', self.gf('django.db.models.fields.CharField')(default=u'', max_length=64, blank=True), keep_default=False)

        # User chose to not deal with backwards NULL issues for 'DMUserProfile.location'
        raise RuntimeError("Cannot reverse this migration. 'DMUserProfile.location' and its values cannot be restored.")

        # Adding field 'DMUserProfile.english_band_score'
        db.add_column('accounts_dmuserprofile', 'english_band_score', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True), keep_default=False)

        # Adding field 'DMUserProfile.hobby'
        db.add_column('accounts_dmuserprofile', 'hobby', self.gf('django.db.models.fields.CharField')(default=u'', max_length=128, blank=True), keep_default=False)

        # Adding field 'DMUserProfile.high_school'
        db.add_column('accounts_dmuserprofile', 'high_school', self.gf('django.db.models.fields.CharField')(default=u'', max_length=32, blank=True), keep_default=False)

        # Adding field 'DMUserProfile.phone'
        db.add_column('accounts_dmuserprofile', 'phone', self.gf('django.db.models.fields.CharField')(default='', max_length=24, blank=True), keep_default=False)

        # Adding field 'DMUserProfile.awards'
        db.add_column('accounts_dmuserprofile', 'awards', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # User chose to not deal with backwards NULL issues for 'DMUserProfile.ethnic'
        raise RuntimeError("Cannot reverse this migration. 'DMUserProfile.ethnic' and its values cannot be restored.")

        # Adding field 'DMUserProfile.nickname'
        db.add_column('accounts_dmuserprofile', 'nickname', self.gf('django.db.models.fields.CharField')(default=u'', max_length=32, blank=True), keep_default=False)

        # Adding field 'DMUserProfile.sign_line'
        db.add_column('accounts_dmuserprofile', 'sign_line', self.gf('django.db.models.fields.CharField')(default=u'', max_length=128, blank=True), keep_default=False)

        # User chose to not deal with backwards NULL issues for 'DMUserProfile.join_date'
        raise RuntimeError("Cannot reverse this migration. 'DMUserProfile.join_date' and its values cannot be restored.")

        # Adding field 'DMUserProfile.klass'
        db.add_column('accounts_dmuserprofile', 'klass', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['classes.LogicalClass'], null=True), keep_default=False)


    models = {
        'accounts.dmuserprofile': {
            'Meta': {'object_name': 'DMUserProfile'},
            'gender': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'zh'", 'max_length': '5'}),
            'mugshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.CharField', [], {'default': "'registered'", 'max_length': '15'}),
            'realname': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'role': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
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
        }
    }

    complete_apps = ['accounts']
