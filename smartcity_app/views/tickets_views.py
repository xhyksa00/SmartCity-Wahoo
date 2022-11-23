from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from ..models import Ticket, User, ServiceRequest
from .helpers import getCurrentUserDict, getLoggedUserObject
from django.contrib import messages
from ..forms.ticket_forms import CreateTicketForm

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

    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            ticket = Ticket(
                title = form.cleaned_data['title'],
                description = form.cleaned_data['description'],
                priority = form.cleaned_data['priority']
            )
            ticket.state = 'Open'
            ticket.authorid = getLoggedUserObject(request)
    else:
        form = CreateTicketForm()
    
    context = {
        'form': form
    }
    return render(request, 'tickets/create.html', context)

