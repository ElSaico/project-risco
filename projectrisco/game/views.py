from django.http import HttpResponseRedirect
from django.contrib.auth import logout as do_logout
from django.template import RequestContext
from django.shortcuts import render_to_response

def render(request, tpl_name, data={}):
   return render_to_response(tpl_name, data, context_instance=RequestContext(request))

def home(request):
   return render(request, 'home.html')

def logout(request):
   do_logout(request)
   return HttpResponseRedirect('/')
