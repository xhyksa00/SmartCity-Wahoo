from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from ..models import Ticket, User, ServiceRequest
from .helpers import getCurrentUserDict, getLoggedUserObject
from django.contrib import messages
from ..forms.request_forms import CreateRequestForm
from django.core.files.storage import FileSystemStorage

# NOTE: DONE!
def list_requests(request: HttpRequest) -> HttpResponse:
    currentUserData = getCurrentUserDict(request)
    if currentUserData == {}:
        messages.warning(request, 'You need to log in to visit this page.')
        return HttpResponseRedirect('/user/login/')

    print(currentUserData)
    if currentUserData['role'] != 'Technician':
        messages.warning(request, 'You don\'t have sufficient rights to access this page.')
        return HttpResponseRedirect('/')

    requests = ServiceRequest.objects.all()
    context = {
        'requests': requests,
        'currentUserData': currentUserData,
    }

    return render(request, 'requests/list.html', context)


# NOTE: DONE!
def show_request(request: HttpRequest, id:int) -> HttpResponse:
    currentUserData = getCurrentUserDict(request)
    if currentUserData == {}:
        messages.warning(request, 'You need to log in to visit this page.')
        return HttpResponseRedirect('/user/login/')
    elif currentUserData['role'] == 'Citizen':
        messages.warning(request, 'You don\'t have sufficient rights to access this page.')
        return HttpResponseRedirect('/')

    serviceRequest = ServiceRequest.objects.filter(id=id).select_related('authorid','technicianid').all().first()

    owner = (serviceRequest.authorid_id == currentUserData['id'])
    context = {
        'serviceRequest': serviceRequest,
        'currentUserData': currentUserData,
        'owner': owner
    }

    return render(request, 'requests/details.html', context)

# TODO:FIXME:
def create_request(request: HttpRequest, ticket_id: int = -1) -> HttpResponse:
    currentUserData = getCurrentUserDict(request)
    if currentUserData == {}:
        messages.warning(request, 'You need to log in to visit this page.')
        return HttpResponseRedirect('/user/login/')

    # pick ticket to assign to
    if request.method == 'POST':
        request_form = CreateRequestForm()
        if ticket_id == -1:
            pass
        else:
            pass


    # if request.method == 'POST':
    #     ticket_form = CreateTicketForm(request.POST)
    #     image_form = UploadImageForm(request.POST, request.FILES)
    #     if ticket_form.is_valid() and image_form.is_valid():
    #         ticket = Ticket(
    #             title = ticket_form.cleaned_data['title'],
    #             description = ticket_form.cleaned_data['description'],
    #             priority = ticket_form.cleaned_data['priority'],
    #             state = 'Open',
    #             authorid_id = request.session['userId'],
    #         )
    #         ticket.save()
            
    #         # Save multiple image urls
    #         urls = request.FILES.getlist('url')
    #         for u in urls:
    #             image = Image(
    #                 url = u,
    #                 ticketid = ticket
    #                 )
    #             image.save()
            
    #         messages.success(request, 'Ticket created.')
    #         return HttpResponseRedirect(f'/tickets/list/{ticket.id}/')
    # else:
    #     ticket_form = CreateTicketForm()
    #     image_form = UploadImageForm()
    
    # context = {
    #     'ticket_form': ticket_form,
    #     'image_form': image_form,
    #     'currentUserData': currentUserData
    # }
    return render(request, 'tickets/create.html', {})

# TODO:FIXME:
def edit_request(request: HttpRequest, id:int) -> HttpResponse:
    currentUserData = getCurrentUserDict(request)
    if currentUserData == {}:
        messages.warning(request, 'You need to log in to visit this page.')
        return HttpResponseRedirect('/user/login/')
    
    # ticket = Ticket.objects.filter(id=id).first()

    # if currentUserData['id'] != ticket.authorid_id:
    #     messages.error(request, 'You do not have permission to visit this page.')
    #     return HttpResponseRedirect('/')

    # if request.method == 'POST':
    #     ticket_form = CreateTicketForm(request.POST, instance=ticket)
    #     ticket_form.save()
    #     messages.success(request,'Ticket changed.')
    #     return HttpResponseRedirect(f'/tickets/list/{id}/')

    # else:
    #     ticket_form = CreateTicketForm(instance=ticket)

    # context = {
    #     'ticket_form': ticket_form,
    #     'currentUserData': currentUserData
    # }

    return render(request, 'tickets/edit.html', {})
