# user_views.py
# Author: Leopold Nemcek
# Description: View functions for user manipulation

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest
from ..forms.user_forms import LoginForm, RegisterForm, OfficerRoleForm, EditAccountForm, ChangePasswordForm, UserFilterForm
from bcrypt import hashpw,gensalt,checkpw
from ..models import LoginInfo, User
from django.contrib import messages
from .helpers import getCurrentUserDict

# View for logging in
def login(request):
    context = {
        'title' : 'Login'
    }
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            context['form'] = form                
            email = form.cleaned_data['email']
            pwd = form.cleaned_data['password']

            # Get login info(email and password) from DB by email
            loginData = LoginInfo.objects.filter(email = email).all()
        
            #If login info was found and password checks out with the hashed password from DB
            if ( loginData and checkpw(pwd.encode('utf8'), loginData.first().password.encode('utf8')) ):
                request.session['userId'] = loginData.first().userid_id
                request.session.set_expiry(0)

                messages.success(request, 'Login succesfull.')
                return HttpResponseRedirect('/')
            else:
                messages.error(request,'Credentials do not match any account.')
                return render(request, 'user/login.html',context)
        else:
            return HttpResponseBadRequest()
    else:
        context['form'] = LoginForm()
        return render(request, 'user/login.html', context=context)

# View for user registration
def register(request):
    context = {
        'title' : 'Register'
    }
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']


            context['form'] = form

            pwd = form.cleaned_data['password']
            # Password and confirm password has to match
            if( pwd == form.cleaned_data['confirm_password']):

                # Check whether wmail isnt already in use
                loginData = LoginInfo.objects.filter(email = email).all()
                if(loginData):
                    messages.error(request, 'E-mail adress is already in use.')
                    return render(request, '/user/register.html', context)

                # Create user in DB
                user = User(
                    name = form.cleaned_data['first_name'],
                    surname = form.cleaned_data['surname'],
                    role = 'citizen'
                )
                user.save()

                # Create login info in DB
                loginInfo = LoginInfo(
                    email = form.cleaned_data['email'],
                    # This method hashes password with salt and then returns it in format <salt><hashed_password>, so we dont need to save salt separatedly
                    password = hashpw(form.cleaned_data['password'].encode('utf8'), gensalt()).decode('utf8'),
                    userid = user
                )

                loginInfo.save()


                messages.success(request, 'Account successfully created.')
                return HttpResponseRedirect('/user/login/')
            else:
                
                messages.error(request, 'Passwords do not match.')
                return render(request, 'user/register.html', context)
    else:
        context['form'] = RegisterForm()
        return render(request, 'user/register.html', context=context)


# This view shows user profiles and allows officers to change their role between citizen and service technician
def viewUser(request, id):
    currentUserData = getCurrentUserDict(request)
    if currentUserData == {}:
        messages.error(request, "You need to log in to visit this page.")
        return HttpResponseRedirect('/user/login/')

    context = {
        'title' : 'View user'
    }

    # Role changing
    if request.method == "POST":
        form = OfficerRoleForm(request.POST)
        if form.is_valid():
            changedUser = User.objects.filter(id = id).all().first()
            changedUser.role = form.cleaned_data['role']
            changedUser.save()
            return HttpResponseRedirect(f'/user/{id}/')


    requestedUserData = User.objects.filter(id = id).values().first()
    if not requestedUserData:
        return HttpResponseBadRequest("User with selected id does not exist")

    context = {**requestedUserData, **context}
    context['currentUserData'] = currentUserData


    # Saving whether the current user is visiting his own profile, so the template will know whether to show buttons for editation and deletion
    if(id == currentUserData['id']):
        context['owner']  = True

    if(currentUserData['role'] == 'officer'):
        form = OfficerRoleForm()
        form.fields['role'].initial = requestedUserData['role']
        context['form'] = form 

    return render(request, 'user/viewUser.html', context)


# Logout view
def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/user/login/')

# View for editing profile
def editProfile(request, id):
    context = {
        'title' : 'Edit account'
    }
    currentUserData = getCurrentUserDict(request)
    if currentUserData == {}:
        messages.warning(request, "You need to log in to visit this page.")
        return HttpResponseRedirect('/user/login/')
    
    # only owner of the profile can edit it
    if currentUserData['id'] != id:
        messages.error(request, 'You do not have permission to visit this page.')
        return HttpResponseRedirect('/')

    # using model form, editation is implemented easily
    if request.method == "POST":
        a = User.objects.filter(id = id).all().first()
        # Get data from form, and fill out rest with the instance
        form = EditAccountForm(request.POST,instance=a)
        form.save()
        request.session['userName'] = form.cleaned_data['name']
        request.session['userSurname'] = form.cleaned_data['surname']
        messages.success(request,'Account changed.')
        return HttpResponseRedirect(f'/user/{id}/')

    else:
        a = User.objects.filter(id = id).all().first()
        form = EditAccountForm(instance=a)
        context['currentUserData']= currentUserData,
        context['form']= form

        return render(request,'user/simpleForm.html',context)


# Account deletion
def deleteAccount(request, id):
    currentUserData = getCurrentUserDict(request)

    if currentUserData['id'] == id :
        User.objects.filter(id = id).delete()
        request.session.flush()
        messages.warning(request, "Account deleted")
        return HttpResponseRedirect('/user/login/')
    elif currentUserData['role'] == 'admin':
        User.objects.filter(id = id).delete()
        messages.warning(request, "Account successfully deleted.")
        return HttpResponseRedirect('/')
    else:
        messages.error(request,"You do not have privileges for this action.")
        return HttpResponseRedirect('/')

# Change of password
def changePassword(request, id):
    currentUserData = getCurrentUserDict(request)
    
    context = {
        'title' : 'Change password'
    }

    if currentUserData == {} or currentUserData['id'] != id:
        messages.error(request, 'You do not have permission to visit this page.')
        return HttpResponseRedirect('/')


    context['currentUserData']= currentUserData

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            oldPwdInput = form.cleaned_data['old_password']
            newPwdInput = form.cleaned_data['password']
            confirmPwdInput = form.cleaned_data['confirm_password']
            context['form'] = form

            if newPwdInput != confirmPwdInput:
                messages.error(request, "Passwords do not match.")
                return render(request, 'user/simpleForm.html', context)
            
            loginInfo = LoginInfo.objects.filter(userid_id = id).all().first()
            if not checkpw(oldPwdInput.encode('utf8'), loginInfo.password.encode('utf8')):
                messages.error(request, "Incorrect password.")
                return render(request, 'user/simpleForm.html', context)

            if oldPwdInput == newPwdInput:
                messages.error(request, "New password cannot be same as old password.")
                return render(request, 'user/simpleForm.html', context)

            loginInfo.password = hashpw(newPwdInput.encode('utf8'),gensalt()).decode('utf8')
            loginInfo.save()
            messages.success(request,'Password changed.')
            return HttpResponseRedirect(f'/user/{id}/')
    
    else:
        context['form'] = ChangePasswordForm()
        return render(request, 'user/simpleForm.html', context)

# View of all users with filtration
def listUsers(request):
    currentUserData = getCurrentUserDict(request)
    if currentUserData == {}:
        messages.error(request, "You need to log in to visit this page.")
        return HttpResponseRedirect('/user/login/')

    context = {
        'title' : 'View users',
        'currentUserData' : currentUserData
    }


    usersSet = User.objects
    if request.method == 'GET':
        form = UserFilterForm(request.GET)
        if form.is_valid():
            cln_data = form.cleaned_data
            # Get filtering data from GET request and then apply filters to Queryset of users one-by-one
            if cln_data['name']:
                usersSet = usersSet.filter(name__icontains = cln_data['name'])

            if cln_data['surname']:
                usersSet = usersSet.filter(surname__icontains = cln_data['surname'])

            if cln_data['role'] and cln_data['role'] != 'any':
                usersSet = usersSet.filter(role = cln_data['role'])

            asc_char = ''
            if cln_data['order'] == 'descending':
                asc_char = '-'

            if cln_data['order_by']:
                usersSet = usersSet.order_by(asc_char + cln_data['order_by'])


    users = usersSet.all()
    context['users'] = users
    context['filter_form'] = form
    return render(request,'user/usersList.html', context)