from django.conf.urls import patterns, include, url

from blog import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', views.home),
	url(r'^', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
