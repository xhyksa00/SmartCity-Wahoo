# helpers.py
# Author: Leopold Nemcek, Rudolf Hyksa
# Description: This file adds helper functions for this app

from ..models import User

def getCurrentUserDict(request):

    if not isUserLogged(request):
        return {}
    
    currentUser = getLoggedUserObject(request)

    return {
        'role' : currentUser.role,
        'name' : currentUser.name,
        'surname' : currentUser.surname,
        'id' : request.session['userId']
    }

def isUserLogged(request):
    if  not 'userId' in request.session:
        request.session.flush()
        return False

    return True

def getLoggedUserObject(request):
    return User.objects.filter(id=request.session['userId']).first()
