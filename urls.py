from django.conf.urls.defaults import patterns, include, url
from TZ import views
from django.contrib.auth.views import login, logout
from django.conf.urls.defaults import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.contrib.comments import urls
#from TZ.views import LatestEntries # redirect

urlpatterns = patterns('',
	(r'^posts/$', views.List_of_posts),
	(r'^profile/$', views.Profile),
	(r'^create/$', views.Create),
	(r'^myposts/$', views.List_of_my_posts),
	(r'^$', views.Login),
	(r'^logout/$', views.Logout),
	(r'^reg/$', views.Reg),	
	url(r'^post/(?P<id>[\d]+)/$', views.View_post),
	# Examples:
	# url(r'^$', 'TZ.views.home', name='home'),
	# url(r'^TZ/', include('TZ.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	url(r'^admin/', include(admin.site.urls)),
		)
