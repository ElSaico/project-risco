from django.conf.urls.defaults import *
from jsonrpc import jsonrpc_site

import game.remote
from game.models import Board, Continent, Territory, Card

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
for model in (Board, Continent, Territory, Card):
	admin.site.register(model)

urlpatterns = patterns('',
    url(r'^call/browse/', 'jsonrpc.views.browse', name='jsonrpc_browser'),
    url(r'^call/', jsonrpc_site.dispatch, name='jsonrpc_mountpoint'),
    url(r'^auth/', include('django_openid_auth.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/(.*)', admin.site.root),
)
