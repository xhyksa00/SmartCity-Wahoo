from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from ..models import Ticket, User, ServiceRequest, Image, TicketComments
from .helpers import getCurrentUserDict, getLoggedUserObject, CommentFull
from django.contrib import messages
from ..forms.ticket_forms import CreateTicketForm, UploadImageForm, CommentForm, PriorityForm, TicketFilterForm, ChangeStateForm
from django.core.files.storage import FileSystemStorage
from django.db.models import Q

def list_tickets(request: HttpRequest) -> HttpResponse:
    currentUserData = getCurrentUserDict(request)
    if currentUserData == {}:
        messages.warning(request, "You need to log in to visit this page.")
        return HttpResponseRedirect('/user/login/')

    ticketsSet = Ticket.objects
    if request.method == 'GET':
        filter_form = TicketFilterForm(request.GET)
        if filter_form.is_valid():
            cln_data = filter_form.cleaned_data
            # Get filtering data from GET request and then apply filters to Queryset of tickets one-by-one
            if cln_data['search']:
                ticketsSet = ticketsSet.filter( Q(title__contains=cln_data['search']) |
                                                Q(description__contains=cln_data['search']))

            if cln_data['priority'] and cln_data['priority'] != 'any':
                ticketsSet = ticketsSet.filter(priority=cln_data['priority'])

            if cln_data['state'] and cln_data['state'] != 'any':
                ticketsSet = ticketsSet.filter(state=cln_data['state'])
            
            ord_char = ''
            if cln_data['order'] == 'dsc':
                ord_char = '-'

            if cln_data['order_by']:
                ticketsSet = ticketsSet.order_by(ord_char + cln_data['order_by'])
    
    tickets = ticketsSet.all()
    context = {
        'title': 'Ticket List',
        'tickets': tickets,
        'filter_form': filter_form,
        'currentUserData': currentUserData,
    }

    return render(request, 'tickets/list.html', context)

def list_created_by(request: HttpRequest, author_id: int) -> HttpResponse:
    currentUserData = getCurrentUserDict(request)
    if currentUserData == {}:
        messages.warning(request, "You need to log in to visit this page.")
        return HttpResponseRedirect('/user/login/')

    ticketsSet = Ticket.objects.filter(authorid_id=author_id)
    if request.method == 'GET':
        filter_form = TicketFilterForm(request.GET)
        if filter_form.is_valid():
            cln_data = filter_form.cleaned_data
            # Get filtering data from GET request and then apply filters to Queryset of tickets one-by-one
            if cln_data['search']:
                ticketsSet = ticketsSet.filter( Q(title__contains=cln_data['search']) |
                                                Q(description__contains=cln_data['search']))

            if cln_data['priority'] and cln_data['priority'] != 'any':
                ticketsSet = ticketsSet.filter(priority=cln_data['priority'])

            if cln_data['state'] and cln_data['state'] != 'any':
                ticketsSet = ticketsSet.filter(state=cln_data['state'])
            
            ord_char = ''
            if cln_data['order'] == 'dsc':
                ord_char = '-'

            if cln_data['order_by']:
                ticketsSet = ticketsSet.order_by(ord_char + cln_data['order_by'])
    
    tickets = ticketsSet.all()
    author = User.objects.filter(id=author_id).first()
    context = {
        'title': 'Ticket List',
        'tickets': tickets,
        'filter_form': filter_form,
        'author': author,
        'currentUserData': currentUserData,
    }

    return render(request, 'tickets/created_by.html', context)

def show_ticket(request: HttpRequest, id:int) -> HttpResponse:
    currentUserData = getCurrentUserDict(request)
    if currentUserData == {}:
        messages.warning(request, "You need to log in to visit this page.")
        return HttpResponseRedirect('/user/login/')

    ticket = Ticket.objects.filter(id=id).select_related('authorid').all().first()
    serviceRequest = ServiceRequest.objects.filter(ticketid = id).all().first()
    images = Image.objects.filter(ticketid=ticket.id).all()

    allow_state_change = (currentUserData['role'] == 'Officer')
    allow_prio_change = (currentUserData['role'] == 'Officer')

    state_change_form = ChangeStateForm(instance=ticket)
    priority_form = PriorityForm(instance=ticket)

    if request.method == 'POST':
        if 'state' in request.POST:
            state_change_form = ChangeStateForm(request.POST)
            if state_change_form.is_valid():
                ticket.state = state_change_form.cleaned_data['state']
                ticket.save()

                messages.success(request,'State changed.')
                return HttpResponseRedirect(f'/tickets/list/{id}/')
        if 'priority' in request.POST:
            priority_form = PriorityForm(request.POST)
            if priority_form.is_valid():
                ticket.priority = priority_form.cleaned_data['priority']
                ticket.save()

                messages.success(request,'Priority changed.')
                return HttpResponseRedirect(f'/tickets/list/{id}/')
        if 'text' in request.POST:
            commentForm = CommentForm(request.POST)
            comment = commentForm.save(commit=False)
            comment.ticketid_id = id
            comment.authorid_id = currentUserData['id']
            comment.save()
            messages.success(request,'Comment added.')

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
        'title': 'Ticket Details',
        'ticket': ticket,
        'serviceRequest': serviceRequest,
        'currentUserData': currentUserData,
        'images': images,
        'owner': owner,
        'comments': fullComments,
        'commentsCount': len(fullComments),
        'comment_form': CommentForm(),
        'priority_form': priority_form,
        'state_change_form': state_change_form,
        'allow_prio_change': allow_prio_change,
        'allow_state_change': allow_state_change,
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
        'title': 'Create Ticket',
        'ticket_form': ticket_form,
        'image_form': image_form,
        'currentUserData': currentUserData
    }
    return render(request, 'tickets/create.html', context)

def edit_ticket(request: HttpRequest, ticket_id:int) -> HttpResponse:
    currentUserData = getCurrentUserDict(request)
    if currentUserData == {}:
        messages.warning(request, "You need to log in to visit this page.")
        return HttpResponseRedirect('/user/login/')
    
    ticket = Ticket.objects.filter(id=ticket_id).first()

    if currentUserData['id'] != ticket.authorid_id:
        messages.error(request, 'You do not have permission to visit this page.')
        return HttpResponseRedirect('/')

    if request.method == "POST":
        ticket_form = CreateTicketForm(request.POST, instance=ticket)
        ticket_form.save()
        messages.success(request,'Ticket changed.')
        return HttpResponseRedirect(f'/tickets/list/{ticket_id}/')

    else:
        ticket_form = CreateTicketForm(instance=ticket)

    context = {
        'title': 'Edit Ticket',
        'ticket_form': ticket_form,
        'currentUserData': currentUserData
    }

    return render(request, 'tickets/edit.html', context)
