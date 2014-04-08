from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.template.defaultfilters import slugify


class Item(models.Model):
	title = models.CharField(max_length=200)
	content = models.CharField(max_length=1000)
	slug = models.SlugField(max_length=200)
	created = models.DateTimeField(timezone.now())

	def save(self):
		self.slug = slugify(self.title)
		post = super(Post, self).save()
		return post

	def __unicode__(self):
		return self.title


