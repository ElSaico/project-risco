from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^call/browse/', 'jsonrpc.views.browse', name='jsonrpc_browser'),
    url(r'^call/(?P<method>[a-zA-Z0-9.-_]+)$', 'game.views.xhr_dispatch'),
    url(r'^call/', 'game.views.xhr_dispatch', name='jsonrpc_mountpoint'),
    url(r'^auth/', include('social_auth.urls')),
    url(r'^auth/logout$', 'game.views.logout', name='logout'),
)
