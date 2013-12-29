import datetime

from django.test import TestCase
from django.utils import timezone

from twitter_clone.models import Post


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
