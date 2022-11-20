from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from bcrypt import hashpw, gensalt, checkpw
from django.contrib import messages
from .helpers import isLoggedIn
from .forms import LoginForm

# Create your views here.


def login(request):
    if isLoggedIn(request):
        # todo: redirect to somewhere meaningful
        return HttpResponse("Already in")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pwdInput = form.cleaned_data['password']

            # TODO: get password from db
            pwd = '$2b$12$Lwi2R63PSbJl3W1a.GZewOeprcNmF3ceRRO1WwWx5jm4ai30Qjtf2'

            if (checkpw(pwdInput.encode('utf8'), pwd.encode('utf8'))):
                request.session['adminName'] = username
                # todo: redirect to somewhere meaningful
                return HttpResponse("HI")
            else:
                messages.error(request, "Incorrect credentials.")
                context = {
                    'form': form,
                    'userName': '',
                    'isLoggedIn': False,
                }
                return render(request, 'login.html', context)
    else:
        form = LoginForm()
        context = {
            'form': form,
            'userName': '',
            'isLoggedIn': False,
        }
        return render(request, 'login.html', context)
