from django.conf.urls.defaults import *
from jsonrpc import jsonrpc_site

import pyWar.remote

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^call/browse/', 'jsonrpc.views.browse', name='jsonrpc_browser'),
    url(r'^call/', jsonrpc_site.dispatch, name='jsonrpc_mountpoint'),
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)
