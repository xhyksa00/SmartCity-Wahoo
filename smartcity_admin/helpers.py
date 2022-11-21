

def isLoggedIn(request):
    return 'adminLoggedIn' in request.session and request.session['adminLoggedIn']