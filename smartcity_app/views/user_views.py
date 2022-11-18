from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest
from ..forms.user_forms import LoginForm, RegisterForm
from bcrypt import hashpw,gensalt,checkpw
from ..models import LoginInfo
from django.contrib import messages


# Create your views here.

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            pwd = form.cleaned_data['password']

            loginData = LoginInfo.objects.filter(email = email)
            
            if ( loginData and checkpw(pwd.encode('utf8'), loginData.password.encode('utf8')) ):
                request.session['userId'] = loginData.user
                return HttpResponseRedirect('/hello/')
            else:
                context = {
                    'form' : form,
                    'login_fail': True
                }
                return render(request, 'user/login.html')
        else:
            return HttpResponseBadRequest()
    else:
        context = {
            'form' : LoginForm(),
            'login_fail': False
        }
        return render(request, 'user/login.html', context=context)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['first_name']
            surname = form.cleaned_data['surname']
            pwd = form.cleaned_data['password']
            pwd_confirm = form.cleaned_data['confirm_password']
            context = { 'email' : email,
            'form' : form,
            'pwdFail' : False,
            'emailTaken' : False
            }
            if( pwd == pwd_confirm):
                messages.info(request, "LOL")
                #messages.add_message(request, messages.INFO, 'Hello world.')
                return HttpResponseRedirect('/user/registerConfiramtion')
            else:
                context['pwdFail']  = True
                return render(request, 'user/register.html', context)
    else:
        context = {'pwdFail' : False,
        'emailTaken': False,
        'form' : RegisterForm()}
        return render(request, 'user/register.html', context=context)

def registerConfirmation(request):
    return render(request,'user/registerConfiramtion.html')

def sayHello(request):
    if 'userId' in request.session:
        email = request.session['userId']
    else:
        email = ''
    return render(request,'hello.html',{'name' : email})