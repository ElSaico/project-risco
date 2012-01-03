from django.conf.urls.defaults import *
from jsonrpc import jsonrpc_site

import game.remote

urlpatterns = patterns('',
    url(r'^call/browse/', 'jsonrpc.views.browse', name='jsonrpc_browser'),
    url(r'^call/(?P<method>[a-zA-Z0-9.-_]+)$', jsonrpc_site.dispatch),
    url(r'^call/', jsonrpc_site.dispatch, name='jsonrpc_mountpoint'),
    url(r'^auth/', include('social_auth.urls')),
    url(r'^auth/logout$', 'game.views.logout', name='logout'),
)
