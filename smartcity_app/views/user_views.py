from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest
from ..forms.user_forms import LoginForm, RegisterForm, OfficerRoleForm, EditAccountForm, ChangePasswordForm
from bcrypt import hashpw,gensalt,checkpw
from ..models import LoginInfo, User
from django.contrib import messages
from .helpers import getCurrentUserDict


# Create your views here.

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

            loginData = LoginInfo.objects.get(email = email)
        

            if ( loginData and checkpw(pwd.encode('utf8'), loginData.password.encode('utf8')) ):
                request.session['userId'] = loginData.userid_id
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
            if( pwd == form.cleaned_data['confirm_password']):

                loginData = LoginInfo.objects.filter(email = email).all()
                if(loginData):
                    messages.error(request, 'Account with this e-mail adress already exists.')
                    return render(request, '/user/register.html', context)

                user = User(
                    name = form.cleaned_data['first_name'],
                    surname = form.cleaned_data['surname'],
                    role = 'citizen'
                )
                user.save()

                loginInfo = LoginInfo(
                    email = form.cleaned_data['email'],
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


def viewUser(request, id):
    currentUserData = getCurrentUserDict(request)
    if currentUserData == {}:
        messages.error(request, "You need to log in to visit this page.")
        return HttpResponseRedirect('/user/login/')

    context = {
        'title' : 'View user'
    }

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



    if(id == currentUserData['id']):
        context['owner']  = True

    if(currentUserData['role'] == 'officer'):
        form = OfficerRoleForm()
        form.fields['role'].initial = requestedUserData['role']
        context['form'] = form 

    return render(request, 'user/viewUser.html', context)



def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/user/login/')

def editProfile(request, id):
    context = {
        'title' : 'Edit account'
    }
    currentUserData = getCurrentUserDict(request)
    if currentUserData == {}:
        messages.warning(request, "You need to log in to visit this page.")
        return HttpResponseRedirect('/user/login/')
    
    if currentUserData['id'] != id:
        messages.error(request, 'You do not have permission to visit this page.')
        return HttpResponseRedirect('/')

    if request.method == "POST":
        a = User.objects.filter(id = id).all().first()
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



def deleteAccount(request, id): #TODO: confirmation?
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