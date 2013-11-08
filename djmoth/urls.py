from django.conf.urls import patterns, url
from moth.views import RouterView, about, home


urlpatterns = patterns('',
    url(r'^about/', about, name='about'),
    url(r'^$', home, name='home'),
    
    # Send all requests to the router!
    url(r'', RouterView()),
)
