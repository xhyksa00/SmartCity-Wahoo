from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from ..forms.user_forms import LoginForm, RegisterForm
from bcrypt import hashpw,gensalt,checkpw

# Create your views here.

def login(request):
    desiredpwd = '$2b$12$GekvU9FMIs0/8sSWTLAEYeyrCQvmFFQbF.9AttkZQsY6yMmqLrQw.'.encode('utf8')

    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            pwd = form.cleaned_data['password'].encode('utf8')
            email = form.cleaned_data['email']
            if ( checkpw(pwd, desiredpwd) ):
                request.session['email'] = email
                return HttpResponseRedirect('/hello/')
            else:
                
                return render(request, 'user/login.html') 

    else:
        context = {'form' : LoginForm(),
        'login_fail': False}
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
    if 'email' in request.session:
        email = request.session['email']
    else:
        email = ''
    return render(request,'hello.html',{'name' : email})