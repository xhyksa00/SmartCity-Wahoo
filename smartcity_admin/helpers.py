# helpers.py
# Author: Leopold Nemcek
# Description: Helper functions for the admin app


def isLoggedIn(request):
    return 'adminLoggedIn' in request.session and request.session['adminLoggedIn']