
def getCurrentUserDict(request):
    if not 'userId' in request.session:
        request.session.flush()
        return {}
    
    return {
        'role' : request.session['userRole'],
        'name' : request.session['userName'],
        'surname' : request.session['userSurname'],
        'id' : request.session['userId']
    }


