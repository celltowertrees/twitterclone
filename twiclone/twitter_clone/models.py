from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User


class UserProfile(models.Model):

    user = models.OneToOneField(User)
    followers = models.ManyToManyField("self", symmetrical=False, related_name="followed_by")
    
    def __unicode__(self):
        return self.user.username

     
    
class Post(models.Model):

    text = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True, blank=True)
    poster = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.text
        
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(minutes=5) <= self.date < now

    def is_editable(self):
        if self.was_published_recently():
            return True
        else:
            return False
            
