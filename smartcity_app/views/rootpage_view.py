# rootpage_view.py
# Author: Leopold Nemcek
# Description: View for behavior on the root page ('/')

from django.http import HttpResponseRedirect
from .helpers import isUserLogged

# Check for login and put user to login screen or to tickets view
def rootPage(request):
    if isUserLogged(request):
        return HttpResponseRedirect('/tickets/list/')
    else:
        return HttpResponseRedirect('/user/login/')