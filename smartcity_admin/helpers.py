

def isLoggedIn(request):
    return 'adminName' in request.session