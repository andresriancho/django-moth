from django.conf.urls import patterns, include, url
from moth.views import RouterView


urlpatterns = patterns('',
    # Send all requests to the router!
    url(r'', RouterView()),
)
