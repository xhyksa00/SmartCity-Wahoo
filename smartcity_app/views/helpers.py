
def getCurrentUserDict(request):
    if not 'userId' in request.session:
        request.session.pop('userRole')
        request.session.pop('userName')
        request.session.pop('userSurname')
        return {}
    
    return {
        'roleCurrent' : request.session['userRole'],
        'nameCurrent' : request.session['userName'],
        'surnameCurrent' : request.session['userSurname'],
        'idCurrent' : request.session['userId']
    }
