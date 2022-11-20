from django.http import HttpResponseRedirect
from .helpers import isUserLogged

def rootPage(request):
    if isUserLogged(request):
        return HttpResponseRedirect('/tickets/list/')
    else:
        return HttpResponseRedirect('/user/login/')