from django.http import HttpResponseRedirect
from django.contrib.auth import logout as do_logout

def logout(request):
   do_logout(request)
   return HttpResponseRedirect('/')
