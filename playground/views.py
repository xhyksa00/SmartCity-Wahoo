from django.shortcuts import render
from django.http import HttpResponse
from .forms.forms import NameForm
from bcrypt import hashpw,gensalt,checkpw

# Create your views here.

def say_hello(request):
    return render(request,'hello.html', {'name': 'k'})

def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            salt = '$2b$12$GekvU9FMIs0/8sSWTLAEYe'.encode('utf8')
            pwd = form.cleaned_data['your_password'].encode('utf8')
            desiredpwd = '$2b$12$GekvU9FMIs0/8sSWTLAEYeyrCQvmFFQbF.9AttkZQsY6yMmqLrQw.'.encode('utf8')
            if ( checkpw(pwd, desiredpwd) ):
                return render(request,'hello.html', {'name': form.cleaned_data['your_name']})
            else:
                return HttpResponse("Access denied.")

    else:
        form = NameForm()
    
    return render(request, 'name.html', {'form': form})