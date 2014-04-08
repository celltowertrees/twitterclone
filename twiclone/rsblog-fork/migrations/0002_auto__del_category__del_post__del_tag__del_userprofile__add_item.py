# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'rsblog-fork_category')

        # Deleting model 'Post'
        db.delete_table(u'rsblog-fork_post')

        # Removing M2M table for field tags on 'Post'
        db.delete_table(db.shorten_name(u'rsblog-fork_post_tags'))

        # Deleting model 'Tag'
        db.delete_table(u'rsblog-fork_tag')

        # Deleting model 'UserProfile'
        db.delete_table(u'rsblog-fork_userprofile')

        # Adding model 'Item'
        db.create_table(u'rsblog-fork_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=200)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'rsblog-fork', ['Item'])


    def backwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'rsblog-fork_category', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=200, unique=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'rsblog-fork', ['Category'])

        # Adding model 'Post'
        db.create_table(u'rsblog-fork_post', (
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rsblog-fork.Category'], null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=200)),
        ))
        db.send_create_signal(u'rsblog-fork', ['Post'])

        # Adding M2M table for field tags on 'Post'
        m2m_table_name = db.shorten_name(u'rsblog-fork_post_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm[u'rsblog-fork.post'], null=False)),
            ('tag', models.ForeignKey(orm[u'rsblog-fork.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'tag_id'])

        # Adding model 'Tag'
        db.create_table(u'rsblog-fork_tag', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=200, unique=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'rsblog-fork', ['Tag'])

        # Adding model 'UserProfile'
        db.create_table(u'rsblog-fork_userprofile', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='Author', unique=True, to=orm['auth.User'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'rsblog-fork', ['UserProfile'])

        # Deleting model 'Item'
        db.delete_table(u'rsblog-fork_item')


    models = {
        u'rsblog-fork.item': {
            'Meta': {'object_name': 'Item'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['rsblog-fork']