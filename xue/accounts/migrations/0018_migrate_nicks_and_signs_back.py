# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):
    def forwards(self, orm):
        CentralStudentInfo = orm['infocenter.CentralStudentInfo']
        for profile in orm.DMUserProfile.objects.all():
            try:
                infoentry = CentralStudentInfo.objects.get(user=profile.user)
            except CentralStudentInfo.DoesNotExist:
                continue

            profile.nickname, profile.sign_line = (
                    infoentry.nickname,
                    infoentry.sign_line,
                    )
            profile.save()

    def backwards(self, orm):
        raise RuntimeError('this migration is not meant to be reversed')

    models = {
        'accounts.dmuserprofile': {
            'Meta': {'object_name': 'DMUserProfile'},
            'gender': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'zh'", 'max_length': '5'}),
            'mugshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '32', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.CharField', [], {'default': "'registered'", 'max_length': '15'}),
            'realname': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'role': ('django.db.models.fields.IntegerField', [], {}),
            'sign_line': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '128', 'blank': 'True'}),
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
            'ident': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'ident_ma': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'ident_pa': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
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

    complete_apps = ['infocenter', 'accounts']


# vim:ai:et:ts=4:sw=4:sts=4:
