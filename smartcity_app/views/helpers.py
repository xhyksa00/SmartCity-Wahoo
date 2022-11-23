from ..models import User

def getCurrentUserDict(request):

    if not isUserLogged(request):
        return {}
    
    return {
        'role' : request.session['userRole'],
        'name' : request.session['userName'],
        'surname' : request.session['userSurname'],
        'id' : request.session['userId']
    }

def isUserLogged(request):
    if not 'userRole' in request.session or not 'userName' in request.session or not 'userSurname' in request.session or not 'userId' in request.session:
        request.session.flush()
        return False

    return True

def getLoggedUserObject(request):
    return User.objects.filter(id=request.session['userId']).first()
