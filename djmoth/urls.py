from django.conf.urls import patterns, url
from moth.views import RouterView, about, home


urlpatterns = patterns('',
    url(r'^about/', about, name='about'),
    url(r'^$', home, name='home'),
    
    # Send all requests that don't match the previous to the router!
    url(r'', RouterView()),
)
