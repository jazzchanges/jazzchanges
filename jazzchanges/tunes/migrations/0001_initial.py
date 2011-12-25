# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Tune'
        db.create_table('tunes_tune', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('key', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('tunes', ['Tune'])

        # Adding model 'Change'
        db.create_table('tunes_change', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('interval', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('beats', self.gf('django.db.models.fields.PositiveIntegerField')(default=4)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('tune', self.gf('django.db.models.fields.related.ForeignKey')(related_name='changes', to=orm['tunes.Tune'])),
        ))
        db.send_create_signal('tunes', ['Change'])


    def backwards(self, orm):
        
        # Deleting model 'Tune'
        db.delete_table('tunes_tune')

        # Deleting model 'Change'
        db.delete_table('tunes_change')


    models = {
        'tunes.change': {
            'Meta': {'ordering': "['order']", 'object_name': 'Change'},
            'beats': ('django.db.models.fields.PositiveIntegerField', [], {'default': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'tune': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'changes'", 'to': "orm['tunes.Tune']"})
        },
        'tunes.tune': {
            'Meta': {'object_name': 'Tune'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['tunes']
