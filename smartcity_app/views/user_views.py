from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest
from ..forms.user_forms import LoginForm, RegisterForm
from bcrypt import hashpw,gensalt,checkpw
from ..models import LoginInfo, User
from django.contrib import messages


# Create your views here.

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            context = {
                'form' : form
            }
            email = form.cleaned_data['email']
            pwd = form.cleaned_data['password']

            # loginData = LoginInfo.objects.filter(email = email).select_related('userid').values()
            loginData = LoginInfo.objects.filter(email = email).values()

            if ( loginData and checkpw(pwd.encode('utf8'), loginData.first()['password'].encode('utf8')) ):
                # request.session['userRole'] = loginData.first()['userid']

                messages.success(request, 'Login succesfull.')
                return render(request, 'user/login.html',context)
            else:
                messages.error(request,'Credentials do not match any account.')
                return render(request, 'user/login.html',context)
        else:
            return HttpResponseBadRequest()
    else:
        context = {
            'form' : LoginForm()
        }
        return render(request, 'user/login.html', context=context)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']


            context = { 
                'form' : form,
            }

            pwd = form.cleaned_data['password']
            if( pwd == form.cleaned_data['confirm_password']):

                loginData = LoginInfo.objects.filter(email = email).values()
                kek = loginData.first()
                if(loginData):
                    messages.error(request, 'Email already taken, id = %i .' % kek)
                    return render('/user/register.html', context)

                user = User(
                    name = form.cleaned_data['first_name'],
                    surname = form.cleaned_data['surname'],
                    role = 'citizen'
                )
                user.save()

                loginInfo = LoginInfo(
                    email = form.cleaned_data['email'],
                    password = hashpw(form.cleaned_data['password'].encode('utf8'), gensalt()),
                    userid = user
                )

                loginInfo.save()


                messages.success(request, 'Account successfully created.')
                return HttpResponseRedirect('/user/login')
            else:
                
                messages.error(request, 'Passwords do not match.')
                return render(request, 'user/register.html', context)
    else:
        context = {'pwdFail' : False,
        'emailTaken': False,
        'form' : RegisterForm()}
        return render(request, 'user/register.html', context=context)


def sayHello(request):
    if 'userId' in request.session:
        email = request.session['userId']
    else:
        email = ''
    return render(request,'hello.html',{'name' : email})