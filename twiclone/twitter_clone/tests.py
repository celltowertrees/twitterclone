import datetime

from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from rebar.testing import flatten_to_dict

from twitter_clone.models import Post, UserProfile
from twitter_clone.forms import CreateUserForm, AuthenticateForm, PostForm


class PostMethodTests(TestCase):

    def test_was_published_recently_with_future_post(self):
        """
        was_published_recently should return False for posts that have a date from the future
        """
        future_post = Post(date=timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(future_post.was_published_recently(), False)
        
    def test_was_published_recently_with_old_post(self):
        """
        was_published_recently() should return False for posts that are older than 5 minutes
        """
        old_post = Post(date=timezone.now() - datetime.timedelta(minutes=5))
        self.assertEqual(old_post.was_published_recently(), False)
        
    def test_was_published_recently_with_recent_post(self):
        """
        was_published_recently() should return True for polls whose date is within 5 minutes
        """
        recent_post = Post(date=timezone.now() - datetime.timedelta(minutes=2))
        self.assertEqual(recent_post.was_published_recently(), True)
    
    def test_is_not_editable(self):
        """
        should return HttpResponseForbidden() for posts that are not recently published
        """
        old_post = Post(date=timezone.now() - datetime.timedelta(minutes=6))
        self.assertEqual(old_post.is_editable(), False)
        
    def test_cache(self):
        """
        should return that the cache has been cleared after a post has been edited
        """
        old_post = Post(date=timezone.now(), text="Old text")
        new_post = Post(date=timezone.now(), text="New text")
        key = make_template_fragment_key('posttemplate', [old_post]) 
        self.assertEqual(cache.get(key), None)
        


class UserMethodTests(TestCase):

    def test_follow(self):
        """
        should assert that user2 is user1's follower
        """
        bob = User(username="bob")
        joe = User(username="joe")
        
        user1 = bob.get_profile()
        user1.followers.add(joe)
        
        self.assertEqual(user1.followers.get(user=joe), joe)
        
    # def user_is_logged_in(self):
    
    # def user_is_logged_out(self):
    
    # def user_can_post(self):
    
    # def user_can_edit(self):
        
    
    # def username_is_email(self):


# class FormTests(TestCase):
    
    # def test_post_published(self):
    
    # def test_post_edited(self):
  
  
# class UrlTests(TestCase):


# class ViewTests(TestCase):

    
    