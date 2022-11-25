from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from ..models import Ticket, User, ServiceRequest, Image
from .helpers import getCurrentUserDict, getLoggedUserObject
from django.contrib import messages
from ..forms.ticket_forms import CreateTicketForm, UploadImageForm
from django.core.files.storage import FileSystemStorage

def list_tickets(request: HttpRequest) -> HttpResponse:
    currentUserData = getCurrentUserDict(request)
    if currentUserData == {}:
        messages.warning(request, "You need to log in to visit this page.")
        return HttpResponseRedirect('/user/login/')

    tickets = Ticket.objects.all()
    context = {
        'tickets': tickets,
        'currentUserData': currentUserData,
    }

    return render(request, 'tickets/list.html', context)

def show_ticket(request: HttpRequest, id:int) -> HttpResponse:
    currentUserData = getCurrentUserDict(request)
    if currentUserData == {}:
        messages.warning(request, "You need to log in to visit this page.")
        return HttpResponseRedirect('/user/login/')

    ticket = Ticket.objects.filter(id=id).select_related('authorid').all().first()
    serviceRequest = ServiceRequest.objects.filter(ticketid = id).all().first()
    images = Image.objects.filter(ticketid=ticket.id).all()

    owner = (ticket.authorid_id == currentUserData['id'])
    context = {
        'ticket': ticket,
        'serviceRequest': serviceRequest,
        'currentUserData': currentUserData,
        'images': images,
        'owner': owner
    }

    return render(request, 'tickets/details.html', context)

def create_ticket(request: HttpRequest) -> HttpResponse:
    currentUserData = getCurrentUserDict(request)
    if currentUserData == {}:
        messages.warning(request, "You need to log in to visit this page.")
        return HttpResponseRedirect('/user/login/')
    if request.method == 'POST':
        ticket_form = CreateTicketForm(request.POST)
        image_form = UploadImageForm(request.POST, request.FILES)
        if ticket_form.is_valid() and image_form.is_valid():
            ticket = Ticket(
                title = ticket_form.cleaned_data['title'],
                description = ticket_form.cleaned_data['description'],
                priority = ticket_form.cleaned_data['priority'],
                state = 'Open',
                authorid_id = request.session['userId'],
            )
            ticket.save()
            
            # Save multiple image urls
            urls = request.FILES.getlist('url')
            for u in urls:
                image = Image(
                    url = u,
                    ticketid = ticket
                    )
                image.save()
            
            messages.success(request, 'Ticket created.')
            return HttpResponseRedirect(f'/tickets/list/{ticket.id}/')
    else:
        ticket_form = CreateTicketForm()
        image_form = UploadImageForm()
    
    context = {
        'ticket_form': ticket_form,
        'image_form': image_form,
        'currentUserData': currentUserData
    }
    return render(request, 'tickets/create.html', context)

def edit_ticket(request: HttpRequest, id:int) -> HttpResponse:
    currentUserData = getCurrentUserDict(request)
    if currentUserData == {}:
        messages.warning(request, "You need to log in to visit this page.")
        return HttpResponseRedirect('/user/login/')
    
    ticket = Ticket.objects.filter(id=id).first()

    if currentUserData['id'] != ticket.authorid_id:
        messages.error(request, 'You do not have permission to visit this page.')
        return HttpResponseRedirect('/')

    if request.method == "POST":
        ticket_form = CreateTicketForm(request.POST, instance=ticket)
        ticket_form.save()
        messages.success(request,'Ticket changed.')
        return HttpResponseRedirect(f'/tickets/list/{id}/')

    else:
        ticket_form = CreateTicketForm(instance=ticket)

    context = {
        'ticket_form': ticket_form,
        'currentUserData': currentUserData
    }

    return render(request, 'tickets/edit.html', context)
