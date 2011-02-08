from django.conf.urls.defaults import *
from jsonrpc import jsonrpc_site

import game.remote

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^call/browse/', 'jsonrpc.views.browse', name='jsonrpc_browser'),
    url(r'^call/', jsonrpc_site.dispatch, name='jsonrpc_mountpoint'),
    url(r'^auth/', include('django_openid_auth.urls')),
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # (r'^admin/(.*)', admin.site.root),
)
