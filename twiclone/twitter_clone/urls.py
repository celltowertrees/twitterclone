from django.conf.urls import patterns, url
from twitter_clone import views

urlpatterns = patterns('twitter_clone.views',
    url(r'^$', views.index, name='index'),
    url(r'^post/(?P<post_id>\d+)/$', views.single_post, name='single_post'),
    url(r'^user/(?P<user_id>\d+)/$', views.profile, name='profile'),
    url(r'^edit/(?P<post_id>\d+)/$', views.edit, name='edit'),
    url(r'^follow/$', views.follow, name='follow'),
    url(r'^create/$', views.create_user, name='create_user'),
    url(r'^submit/$', views.submit, name="submit"),
    url(r'^login/$', views.login_user, name="login_user"),
    url(r'^logout/$', views.logout_user, name="logout_user"),
)
