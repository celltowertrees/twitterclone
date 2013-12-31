import datetime

from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

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
        
    # def test_is_editable(self):
    
    
# class LoginTests(TestCase):

    # def user_is_logged_in(self):
    
    # def user_is_logged_out(self):
    
    # def user_can_post(self):
    
    # def user_can_edit(self):


class UserMethodTests(TestCase):

    def test_follow(self):
        """
        should assert that user2 is user1's follower
        """
        bob = User(username="bob")
        joe = User(username="joe")
        user1 = UserProfile(user=bob)
        user2 = UserProfile(user=joe)
        user1.followers.add(user2)
        
        self.assertEqual(user1.followers.get(username="joe"), user2)
        
    
    # def username_is_email(self):


# class FormTests(TestCase):
    
    # def test_post_published(self):
    
    # def test_post_edited(self):
  
  
# class UrlTests(TestCase):


# class ViewTests(TestCase):

    
    