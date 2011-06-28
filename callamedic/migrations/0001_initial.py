# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Responder'
        db.create_table('callamedic_responder', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('organization', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('android_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('on_call', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('certificate_valid_to', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('callamedic', ['Responder'])

        # Adding model 'Incident'
        db.create_table('callamedic_incident', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=6)),
        ))
        db.send_create_signal('callamedic', ['Incident'])

        # Adding model 'ResponderLocation'
        db.create_table('callamedic_responderlocation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('responder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['callamedic.Responder'])),
        ))
        db.send_create_signal('callamedic', ['ResponderLocation'])

        # Adding model 'IncidentResponder'
        db.create_table('callamedic_incidentresponder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('responder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['callamedic.Responder'])),
            ('incident', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['callamedic.Incident'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('contacted_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('callamedic', ['IncidentResponder'])


    def backwards(self, orm):
        
        # Deleting model 'Responder'
        db.delete_table('callamedic_responder')

        # Deleting model 'Incident'
        db.delete_table('callamedic_incident')

        # Deleting model 'ResponderLocation'
        db.delete_table('callamedic_responderlocation')

        # Deleting model 'IncidentResponder'
        db.delete_table('callamedic_incidentresponder')


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
        'callamedic.incident': {
            'Meta': {'object_name': 'Incident'},
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'responders': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['callamedic.Responder']", 'through': "orm['callamedic.IncidentResponder']", 'symmetrical': 'False'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        'callamedic.incidentresponder': {
            'Meta': {'object_name': 'IncidentResponder'},
            'contacted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incident': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['callamedic.Incident']"}),
            'responder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['callamedic.Responder']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'callamedic.responder': {
            'Meta': {'object_name': 'Responder', '_ormbases': ['auth.User']},
            'android_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'certificate_valid_to': ('django.db.models.fields.DateTimeField', [], {}),
            'on_call': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'organization': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'callamedic.responderlocation': {
            'Meta': {'object_name': 'ResponderLocation'},
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'responder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['callamedic.Responder']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['callamedic']
