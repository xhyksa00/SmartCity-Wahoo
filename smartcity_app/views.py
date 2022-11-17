from django.shortcuts import render
from django.http import HttpResponse
from .forms.forms import LoginForm
from bcrypt import hashpw,gensalt,checkpw

# Create your views here.

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            salt = '$2b$12$GekvU9FMIs0/8sSWTLAEYe'.encode('utf8')
            pwd = form.cleaned_data['password'].encode('utf8')
            desiredpwd = '$2b$12$GekvU9FMIs0/8sSWTLAEYeyrCQvmFFQbF.9AttkZQsY6yMmqLrQw.'.encode('utf8')
            if ( checkpw(pwd, desiredpwd) ):
                return render(request,'hello.html', {'name': form.cleaned_data['name']})
            else:
                return HttpResponse("Access denied.")

    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form.as_table})