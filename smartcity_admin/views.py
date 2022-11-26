# views.py
# Author: Leopold Nemcek
# Description: View functions for admin module

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from bcrypt import hashpw, gensalt, checkpw
from django.contrib import messages
from .helpers import isLoggedIn
from .forms import LoginForm, ChangePasswordForm, RoleChangeForm, UserFilterForm
from .models import AdminInfo, User



# Login page
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
                request.session.set_expiry(0)
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

# Logout function
def logout(request):
    request.session.flush()
    messages.warning(request, 'Logged out.')
    return HttpResponseRedirect('/admin/login/')

# Change password function
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

# View of all users with filtration
def usersList(request):
    if not isLoggedIn(request):
        messages.error(request, 'You need to login first.')
        return HttpResponseRedirect('/admin/login/')

    context = {
        'isLoggedIn': True,
    }

    usersSet = User.objects
    if request.method == 'GET':
        form = UserFilterForm(request.GET)
        if form.is_valid():
            # Get filtering data from GET request and then apply filters to Queryset of users one-by-one
            cln_data = form.cleaned_data

            if cln_data['name']:
                usersSet = usersSet.filter(name__icontains = cln_data['name'])

            if cln_data['surname']:
                usersSet = usersSet.filter(surname__icontains = cln_data['surname'])

            if cln_data['role'] and cln_data['role'] != 'any':
                usersSet = usersSet.filter(role = cln_data['role'])

            if cln_data['id']:
                usersSet = usersSet.filter(id = cln_data['id'])

            asc_char = ''
            if cln_data['order'] == 'descending':
                asc_char = '-'

            if cln_data['order_by']:
                usersSet = usersSet.order_by(asc_char + cln_data['order_by'])


    users = usersSet.all()
    context['users'] = users
    context['filter_form'] = form
    return render(request,'users_list.html', context)

# View single user identified by id
# This view also can also change user's role
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

# View for deleting user identified by id
def deleteUser(request, id):
    if not isLoggedIn(request):
        messages.error(request, 'You need to login first.')
        return HttpResponseRedirect('/admin/')

    User.objects.filter(id = id).delete()
    messages.warning(request, "Account successfully deleted.")
    return HttpResponseRedirect('/admin/')