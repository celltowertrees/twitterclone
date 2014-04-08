from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('rsblog-fork.views',
	url(r'^$', views.index, name='index'),
	url(r'^(?P<item>.+)/$', views.single_item, name='single-item'),
	# url(r'^admin/', include(admin.site.urls)),
	)