from django.core.cache.utils import make_template_fragment_key
from django.db.models.signals import pre_save
from django.dispatch import receiver
from twitter_clone.models import Post
from django.core.cache import cache
 
@receiver(pre_save, sender=Post)
def clear_cache(sender, instance, **kwargs):
    key = make_template_fragment_key('posttemplate', [instance]) 
    if instance is not None:
        cache.delete(key)