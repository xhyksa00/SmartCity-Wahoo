from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from ..models import Ticket, User

def list_tickets(request: HttpRequest) -> HttpResponse:
    data = Ticket.objects.all()
    return render(request, 'tickets/list.html', {'tickets': data})