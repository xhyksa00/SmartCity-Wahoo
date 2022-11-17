from django.shortcuts import render
from django.http import HttpResponse
from ..forms.user_forms import LoginForm
from bcrypt import hashpw,gensalt,checkpw

# Create your views here.

def login(request):
    desiredpwd = '$2b$12$GekvU9FMIs0/8sSWTLAEYeyrCQvmFFQbF.9AttkZQsY6yMmqLrQw.'.encode('utf8')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            pwd = form.cleaned_data['password'].encode('utf8')
            email = form.cleaned_data['email']
            context = { 'name': email }
            if ( checkpw(pwd, desiredpwd) ):
                return render(request,'hello.html', context=context)
            else:
                return HttpResponse("Access denised.")

    else:
        form = LoginForm()
        context = {'form' : form}
    return render(request, 'user/login.html', context=context)