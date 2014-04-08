from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^c/', include('rsblog-fork.urls', namespace="c")),
    url(r'^feed/', include('twitter_clone.urls', namespace="feed")),
    url(r'^admin/', include(admin.site.urls)),
)
