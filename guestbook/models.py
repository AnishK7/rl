from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Comment(models.Model):
	name =  models.CharField(max_length=20)
	comment =  models.TextField()
	date_added = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return '<Name: {},ID: {}>'.format(self.name,self.comment)

