from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given email address must be set')
        email = UserManager.normalize_email(email)
        user = self.model(email=email, is_superuser=False, is_staff=False, is_active=True, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(AbstractBaseUser, PermissionsMixin):
    is_staff = models.BooleanField(('staff status'), default=False)
    is_active = models.BooleanField(('active'), default=True)
    date_joined = models.DateTimeField(('date joined'), default=timezone.now())
    email = models.EmailField('email address', unique=True)
    
    following = models.ManyToManyField("self", through='Relationship', symmetrical=False, related_name="followed_by")
    
    USERNAME_FIELD = 'email'
    objects = UserManager()
    
    def __unicode__(self):
        return self.email
        
    def get_short_name(self):
        """ Only for the admin really """
        return self.email
        
    def get_relationships(self, status):
        return self.following.filter(
            to_user__status=status,
            to_user__from_user=self)
            
    def get_related_to(self, status):
        return self.followed_by.filter(
            from_user__status=status,
            from_user__to_user=self)
            
    def get_following(self):
        return self.get_relationships(RELATIONSHIP_FOLLOWING)
        
    def get_followers(self):
        return self.get_related_to(RELATIONSHIP_FOLLOWING)
        
    def add_relationship(self, user, status):
        relationship, created = Relationship.objects.get_or_create(
            from_user=self, 
            to_user=user,
            status=status)
        return relationship
        
    def remove_relationship(self, user, status):
        Relationship.objects.filter(
            from_user=self, 
            to_user=user,
            status=status).delete()
        return
  
  
RELATIONSHIP_FOLLOWING = 1
RELATIONSHIP_BLOCKED = 2
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_FOLLOWING, 'Following'),
    (RELATIONSHIP_BLOCKED, 'Blocked'),
)
    
    
class Relationship(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user')
    to_user = models.ForeignKey(User, related_name='to_user')
    status = models.IntegerField(choices=RELATIONSHIP_STATUSES)
        

    
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
            
