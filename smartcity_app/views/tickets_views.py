from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from ..models import Ticket, User, ServiceRequest, Image, TicketComments
from .helpers import getCurrentUserDict, getLoggedUserObject, CommentFull
from django.contrib import messages
from ..forms.ticket_forms import CreateTicketForm, UploadImageForm, CommentForm, PriorityForm
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

    if request.method == 'POST':
        if 'text' in request.POST:
            commentForm = CommentForm(request.POST)
            comment = commentForm.save(commit=False)
            comment.ticketid_id = id
            comment.authorid_id = currentUserData['id']
            comment.save()
            messages.success(request,'Comment added.')
        if 'priority' in request.POST:
            priorityFormPOST = PriorityForm(request.POST)
            if priorityFormPOST.is_valid():
                ticket.priority = priorityFormPOST.cleaned_data['priority']
                ticket.save()

    

    priorityForm = PriorityForm()
    priorityForm.fields['priority'].initial = ticket.priority
    comments = TicketComments.objects.filter( ticketid_id = id).all()
    fullComments = []
    for comment in comments:
        fullComment = CommentFull()
        fullComment.text = comment.text
        fullComment.timestamp = comment.created_timestamp
        author = User.objects.filter(id = comment.authorid_id).all()
        if author:
            fullComment.AuthorName = author.first().name + ' ' + author.first().surname
            fullComment.AuthorId = comment.authorid_id
        else:
            fullComment.AuthorName = '[Deleted user]'
        fullComments.append(fullComment)
    
    owner = (ticket.authorid_id == currentUserData['id'])
    context = {
        'ticket': ticket,
        'serviceRequest': serviceRequest,
        'currentUserData': currentUserData,
        'images': images,
        'owner': owner
    }

    context['comments'] = fullComments
    context['comment_form'] = CommentForm()
    context['priority_form'] = priorityForm

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
