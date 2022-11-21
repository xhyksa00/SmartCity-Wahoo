from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from ..models import Ticket, User, ServiceRequest
from .helpers import getCurrentUserDict
from django.contrib import messages
# from ..forms.ticket_forms import CreateTicketForm

def list_tickets(request: HttpRequest) -> HttpResponse:
    tickets = Ticket.objects.all()
    currentUserData = getCurrentUserDict(request)
    context = {
        'tickets': tickets,
        'currentUserData': currentUserData,
    }

    return render(request, 'tickets/list.html', context)

def show_ticket(request: HttpRequest, id:int) -> HttpResponse:
    details = Ticket.objects.filter(id=id).select_related('authorid').all().first()
    serviceRequest = ServiceRequest.objects.filter(ticketid = id).all().first()
    currentUserData = getCurrentUserDict(request)
    context = {
        'ticket': details,
        'serviceRequest': serviceRequest,
        'currentUserData': currentUserData,
    }

    return render(request, 'tickets/details.html', context)

def create_ticket(request: HttpRequest) -> HttpResponse:
    context = {}



    return render(request, 'tickets/create.html', context)

