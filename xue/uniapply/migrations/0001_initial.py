# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Target'
        db.create_table('uniapply_target', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('desc', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('pagelink', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('allow_blank_reason', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('uniapply', ['Target'])

        # Adding M2M table for field allowed_classes on 'Target'
        db.create_table('uniapply_target_allowed_classes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('target', models.ForeignKey(orm['uniapply.target'], null=False)),
            ('logicalclass', models.ForeignKey(orm['classes.logicalclass'], null=False))
        ))
        db.create_unique('uniapply_target_allowed_classes', ['target_id', 'logicalclass_id'])

        # Adding model 'AuditingRule'
        db.create_table('uniapply_auditingrule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uniapply.Target'])),
            ('auditer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('niceness', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('uniapply', ['AuditingRule'])

        # Adding model 'AuditOutcome'
        db.create_table('uniapply_auditoutcome', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uniapply.Target'])),
            ('rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uniapply.AuditingRule'])),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('uniapply', ['AuditOutcome'])

        # Adding model 'UniApplicationEntry'
        db.create_table('uniapply_uniapplicationentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['uniapply.Target'])),
            ('reason', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('uniapply', ['UniApplicationEntry'])


    def backwards(self, orm):
        
        # Deleting model 'Target'
        db.delete_table('uniapply_target')

        # Removing M2M table for field allowed_classes on 'Target'
        db.delete_table('uniapply_target_allowed_classes')

        # Deleting model 'AuditingRule'
        db.delete_table('uniapply_auditingrule')

        # Deleting model 'AuditOutcome'
        db.delete_table('uniapply_auditoutcome')

        # Deleting model 'UniApplicationEntry'
        db.delete_table('uniapply_uniapplicationentry')


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
        'uniapply.auditingrule': {
            'Meta': {'object_name': 'AuditingRule'},
            'auditer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'niceness': ('django.db.models.fields.IntegerField', [], {}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['uniapply.Target']"})
        },
        'uniapply.auditoutcome': {
            'Meta': {'object_name': 'AuditOutcome'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'rule': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['uniapply.AuditingRule']"}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['uniapply.Target']"})
        },
        'uniapply.target': {
            'Meta': {'object_name': 'Target'},
            'allow_blank_reason': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allowed_classes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['classes.LogicalClass']", 'symmetrical': 'False'}),
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'pagelink': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'uniapply.uniapplicationentry': {
            'Meta': {'object_name': 'UniApplicationEntry'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['uniapply.Target']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['uniapply']
