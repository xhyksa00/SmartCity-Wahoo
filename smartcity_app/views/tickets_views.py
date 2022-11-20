from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from ..models import Ticket, User
from .helpers import getCurrentUserDict
from django.contrib import messages
from ..forms import ticket_forms

def list_tickets(request: HttpRequest) -> HttpResponse:
    tickets = Ticket.objects.all()
    return render(request, 'tickets/list.html', {'tickets': tickets})

def show_ticket(request: HttpRequest, id:int) -> HttpResponse:
    ticket = Ticket.objects.filter(id=id).values().first()
    return render(request, 'tickets/details.html', ticket)
