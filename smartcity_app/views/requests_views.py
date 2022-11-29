from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from ..models import Ticket, User, ServiceRequest, ServiceRequestComments
from .helpers import getCurrentUserDict, getLoggedUserObject, CommentFull
from django.contrib import messages
from ..forms.request_forms import CreateRequestForm, AssignTechnicianForm, ServiceRCommentForm, RequestFilterForm, PriorityForm
from django.core.files.storage import FileSystemStorage
from django.db.models import Q

def list_requests(request: HttpRequest) -> HttpResponse:
    currentUserData = getCurrentUserDict(request)
    if currentUserData == {}:
        messages.warning(request, 'You need to log in to visit this page.')
        return HttpResponseRedirect('/user/login/')

    if currentUserData['role'] not in ['Technician', 'Officer']:
        messages.warning(request, 'You don\'t have sufficient rights to access this page.')
        return HttpResponseRedirect('/')

    requestSet = ServiceRequest.objects.select_related('ticketid')

    if request.method == 'GET':
        filter_form = RequestFilterForm(request.GET)
        if filter_form.is_valid():
            cln_data = filter_form.cleaned_data
            # Get filtering data from GET request and then apply filters to Queryset of tickets one-by-one
            if cln_data['search']:
                requestSet = requestSet.filter( Q(ticketid__title__contains=cln_data['search']) |
                                                Q(description__contains=cln_data['search']))

            if cln_data['priority'] and cln_data['priority'] != 'any':
                requestSet = requestSet.filter(priority=cln_data['priority'])

            if cln_data['state'] and cln_data['state'] != 'any':
                requestSet = requestSet.filter(state=cln_data['state'])
            
            ord_char = ''
            if cln_data['order'] == 'dsc':
                ord_char = '-'

            if cln_data['order_by']:
                requestSet = requestSet.order_by(ord_char + cln_data['order_by'])

    requests = requestSet.all()
    context = {
        'title': 'Request List',
        'requests': requests,
        'filter_form': filter_form,
        'currentUserData': currentUserData,
    }

    return render(request, 'requests/list.html', context)

def list_cerated_by(request: HttpRequest, author_id:int) -> HttpResponse:
    currentUserData = getCurrentUserDict(request)
    if currentUserData == {}:
        messages.warning(request, 'You need to log in to visit this page.')
        return HttpResponseRedirect('/user/login/')

    if currentUserData['role'] not in ['Technician', 'Officer']:
        messages.warning(request, 'You don\'t have sufficient rights to access this page.')
        return HttpResponseRedirect('/')

    requestSet = ServiceRequest.objects.filter(authorid_id=author_id).select_related('ticketid')
    author = User.objects.filter(id=author_id).first()
    print(author)

    if request.method == 'GET':
        filter_form = RequestFilterForm(request.GET)
        if filter_form.is_valid():
            cln_data = filter_form.cleaned_data
            # Get filtering data from GET request and then apply filters to Queryset of tickets one-by-one
            if cln_data['search']:
                requestSet = requestSet.filter( Q(ticketid__title__contains=cln_data['search']) |
                                                Q(description__contains=cln_data['search']))

            if cln_data['priority'] and cln_data['priority'] != 'any':
                requestSet = requestSet.filter(priority=cln_data['priority'])

            if cln_data['state'] and cln_data['state'] != 'any':
                requestSet = requestSet.filter(state=cln_data['state'])
            
            ord_char = ''
            if cln_data['order'] == 'dsc':
                ord_char = '-'

            if cln_data['order_by']:
                requestSet = requestSet.order_by(ord_char + cln_data['order_by'])

    requests = requestSet.all()
    context = {
        'title': 'Request List',
        'requests': requests,
        'filter_form': filter_form,
        'author': author,
        'currentUserData': currentUserData,
    }

    return render(request, 'requests/created_by.html', context)

#TODO:
def list_assigned_to(request: HttpRequest, assignee_id: int) -> HttpResponse:
    currentUserData = getCurrentUserDict(request)
    if currentUserData == {}:
        messages.warning(request, 'You need to log in to visit this page.')
        return HttpResponseRedirect('/user/login/')

    if currentUserData['role'] not in ['Technician', 'Officer']:
        messages.warning(request, 'You don\'t have sufficient rights to access this page.')
        return HttpResponseRedirect('/')

    requestSet = ServiceRequest.objects.filter(technicianid_id=assignee_id).select_related('ticketid')

    if request.method == 'GET':
        filter_form = RequestFilterForm(request.GET)
        if filter_form.is_valid():
            cln_data = filter_form.cleaned_data
            # Get filtering data from GET request and then apply filters to Queryset of tickets one-by-one
            if cln_data['search']:
                requestSet = requestSet.filter( Q(ticketid__title__contains=cln_data['search']) |
                                                Q(description__contains=cln_data['search']))

            if cln_data['priority'] and cln_data['priority'] != 'any':
                requestSet = requestSet.filter(priority=cln_data['priority'])

            if cln_data['state'] and cln_data['state'] != 'any':
                requestSet = requestSet.filter(state=cln_data['state'])
            
            ord_char = ''
            if cln_data['order'] == 'dsc':
                ord_char = '-'

            if cln_data['order_by']:
                requestSet = requestSet.order_by(ord_char + cln_data['order_by'])

    requests = requestSet.all()
    assignee = User.objects.filter(id=assignee_id).first()
    context = {
        'title': 'Request List',
        'requests': requests,
        'filter_form': filter_form,
        'assignee': assignee,
        'currentUserData': currentUserData,
    }

    return render(request, 'requests/assigned_to.html', context)

# TODO: Finish HTML - requests/details.html
def show_request(request: HttpRequest, id:int) -> HttpResponse:
    currentUserData = getCurrentUserDict(request)
    if currentUserData == {}:
        messages.warning(request, 'You need to log in to visit this page.')
        return HttpResponseRedirect('/user/login/')
    elif currentUserData['role'] == 'Citizen':
        messages.warning(request, 'You don\'t have sufficient rights to access this page.')
        return HttpResponseRedirect('/')

    serviceRequest = ServiceRequest.objects.filter(id=id).select_related('authorid','technicianid').all().first()
    print(serviceRequest.authorid)
    assign_form = {}
    if currentUserData['role'] == 'Officer':
        # technician = serviceRequest.technicianid
        if request.method == 'POST':
            if 'technicianid' in request.POST:
                assign_form = AssignTechnicianForm(request.POST)
                if assign_form.is_valid():
                    serviceRequest.technicianid = assign_form.cleaned_data['technicianid']
                    serviceRequest.save()

                    messages.success(request,'Technician assigned.')
                    return HttpResponseRedirect(f'/requests/list/{id}/')
            else:
                commentForm = ServiceRCommentForm(request.POST)
                comment = commentForm.save(commit=False)
                comment.requestid_id = id
                comment.authorid_id = currentUserData['id']
                comment.save()
                messages.success(request,'Comment added.')
                assign_form = AssignTechnicianForm(instance=serviceRequest)
        else:
            assign_form = AssignTechnicianForm(instance=serviceRequest)
            # if serviceRequest.technicianid:
            #     assign_form.fields['technicianid'].initial = serviceRequest.technicianid.name + ' ' + serviceRequest.technicianid.surname
            # else:
            #     assign_form.fields['technicianid'].initial = 'none'

    is_assignee = False
    priority_form = {}
    if currentUserData['id'] == serviceRequest.technicianid_id:
        is_assignee = True
        if request.method == 'POST':
            priority_form = PriorityForm(request.POST)
            if priority_form.is_valid():
                serviceRequest.priority = priority_form.cleaned_data['priority']
                serviceRequest.save()

                messages.success(request,'Priority changed.')
                return HttpResponseRedirect(f'/requests/list/{id}/')
        else:
            priority_form = PriorityForm(instance=serviceRequest)

    owner = (serviceRequest.authorid_id == currentUserData['id'])
    comments = ServiceRequestComments.objects.filter(requestid_id = id).all()
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

    context = {
        'title': 'Request Details',
        'serviceRequest': serviceRequest,
        'currentUserData': currentUserData,
        'assign_form': assign_form,
        'priority_form': priority_form,
        'is_assignee': is_assignee,
        'owner': owner,
        'comments' : fullComments,
        'commentsCount' : len(fullComments),
        'comment_form' : ServiceRCommentForm()
    }

    return render(request, 'requests/details.html', context)

def create_request(request: HttpRequest, ticket_id: int = -1) -> HttpResponse:
    currentUserData = getCurrentUserDict(request)
    if currentUserData == {}:
        messages.warning(request, 'You need to log in to visit this page.')
        return HttpResponseRedirect('/user/login/')

    if request.method == 'POST':
        request_form = CreateRequestForm(request.POST)
        if request_form.is_valid():
            serviceRequest = ServiceRequest(
                ticketid = request_form.cleaned_data['ticketid'],
                technicianid = request_form.cleaned_data['technicianid'],
                description = request_form.cleaned_data['description'],
                priority = request_form.cleaned_data['priority'],
                state = 'Open',
                authorid_id = request.session['userId']
            )

            serviceRequest.save()
            messages.success(request,'Request created.')
            return HttpResponseRedirect(f'/requests/list/{serviceRequest.id}')

    # Pick ticket to assign to
    else:
        # Creating a blank request
        if ticket_id == -1:
            request_form = CreateRequestForm()
        # Creating a request to the ticket with ticket_id
        else:
            request_form = CreateRequestForm(tid=ticket_id)


    context = {
        'title': 'Create Service Request',
        'request_form': request_form,
        'currentUserData': currentUserData
    }

    return render(request, 'requests/create.html', context)

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
