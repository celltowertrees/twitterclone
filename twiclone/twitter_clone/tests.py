import datetime

from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from rebar.testing import flatten_to_dict

from twitter_clone.models import Post, User, Relationship, RELATIONSHIP_FOLLOWING
from twitter_clone.forms import CreateUserForm, AuthenticateForm, PostForm


class PostMethodTests(TestCase):

    def test_was_published_recently_with_future_post(self):
        """
        was_published_recently() should return False for posts that have a date from the future
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
        should assert that joe is bob's follower
        """
        bob = User.objects.create(email="bob@bob.com")
        joe = User.objects.create(email="joe@joe.com")
        
        joe.add_relationship(bob, RELATIONSHIP_FOLLOWING)
        
        def iterate(list):
            for i in list:
                return i
        
        self.assertEqual(iterate(bob.get_followers()), joe)
        
    