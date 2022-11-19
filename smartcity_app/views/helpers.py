
def getCurrentUserDict(request):
    if not 'userId' in request.session:
        request.session.flush()
        return {}
    
    return {
        'roleCurrent' : request.session['userRole'],
        'nameCurrent' : request.session['userName'],
        'surnameCurrent' : request.session['userSurname'],
        'idCurrent' : request.session['userId']
    }
