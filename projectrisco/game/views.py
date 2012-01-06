from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout as do_logout
from jsonrpc import jsonrpc_site

def xhr_dispatch(request): 
	if request.method == "OPTIONS":
		response = HttpResponse()
		response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
		response['Access-Control-Allow-Headers'] = 'Content-Type'
		response['Access-Control-Max-Age'] = '1728000'
	else:
		# TODO: servidor cospe erros 403 nesse ponto. talvez aqueles campos extras de aceitar autenticacoes/etc?
		response = jsonrpc_site.dispatch(request)
	response['Access-Control-Allow-Origin'] = '*'
	return response

def logout(request):
   do_logout(request)
   return HttpResponseRedirect('/')
