from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from bcrypt import hashpw, gensalt, checkpw
from django.contrib import messages
from .helpers import isLoggedIn
from .forms import LoginForm, ChangePasswordForm, RoleChangeForm
from .models import AdminInfo, User

# Create your views here.


def login(request):
    if isLoggedIn(request):
        return HttpResponseRedirect('/admin/user/list/')

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pwdInput = form.cleaned_data['password']

            loginInfo = AdminInfo.objects.all().first()
            pwd = loginInfo.password

            if (checkpw(pwdInput.encode('utf8'), pwd.encode('utf8'))):
                request.session['adminLoggedIn'] = True
                messages.success(request, 'Logged in as administrator.')
                return HttpResponseRedirect('/admin/user/list/')
            else:
                messages.error(request, "Incorrect credentials.")
                context = {
                    'form': form,
                    'isLoggedIn': False,
                }
                return render(request, 'login.html', context)
    else:
        form = LoginForm()
        context = {
            'form': form,
            'isLoggedIn': False,
        }
        return render(request, 'login.html', context)


def logout(request):
    request.session.flush()
    messages.warning(request, 'Logged out.')
    return HttpResponseRedirect('/admin/login/')


def changePassword(request):
    if not isLoggedIn(request):
        messages.error(request, 'You need to login first.')
        return HttpResponseRedirect('/admin/login/')

    context = {
        'isLoggedIn': True,
    }

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            oldPwdInput = form.cleaned_data['old_password']
            newPwdInput = form.cleaned_data['password']
            confirmPwdInput = form.cleaned_data['confirm_password']
            context['form'] = form

            if newPwdInput != confirmPwdInput:
                messages.error(request, "Passwords do not match.")
                return render(request, 'simple_form.html', context)

            loginInfo = AdminInfo.objects.all().first()
            if not checkpw(oldPwdInput.encode('utf8'), loginInfo.password.encode('utf8')):
                messages.error(request, "Incorrect password.")
                return render(request, 'simple_form.html', context)

            if oldPwdInput == newPwdInput:
                messages.error(
                    request, "New password cannot be same as old password.")
                return render(request, 'simple_form.html', context)

            loginInfo.password = hashpw(
                newPwdInput.encode('utf8'), gensalt()).decode('utf8')
            loginInfo.save()
            messages.success(request, 'Password changed.')
            return HttpResponseRedirect('/admin/')

    else:
        context['form'] = ChangePasswordForm()
        return render(request, 'simple_form.html', context)


def usersList(request):
    if not isLoggedIn(request):
        messages.error(request, 'You need to login first.')
        return HttpResponseRedirect('/admin/login/')

    context = {
        'isLoggedIn': True,
    }

    users = User.objects.all()

    context['users'] = users

    return render(request,'users_list.html', context)

def viewUser(request, id):
    if not isLoggedIn(request):
        messages.error(request, 'You need to login first.')
        return HttpResponseRedirect('/admin/')

    context = {
        'isLoggedIn': True,
    }

    if request.method == "POST":
        form = RoleChangeForm(request.POST)
        if form.is_valid():
            changedUser = User.objects.filter(id = id).all().first()
            changedUser.role = form.cleaned_data['role']
            changedUser.save()
            messages.success(request, 'User role changed.')
            return HttpResponseRedirect(f'/admin/user/{id}/')


    requestedUserData = User.objects.filter(id = id).values().first()
    if not requestedUserData:
        messages.error(request, 'User with selected ide does not extist')
        return HttpResponseRedirect('/admin/')

    context = {**requestedUserData, **context}

    form = RoleChangeForm( initial = { 'role' : requestedUserData['role']})
    context['form'] = form

    return render(request, 'view_user.html', context)

def deleteUser(request, id):
    if not isLoggedIn(request):
        messages.error(request, 'You need to login first.')
        return HttpResponseRedirect('/admin/')

    User.objects.filter(id = id).delete()
    messages.warning(request, "Account successfully deleted.")
    return HttpResponseRedirect('/admin/')