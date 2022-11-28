from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from ..models import Ticket, User, ServiceRequest, ServiceRequestComments
from .helpers import getCurrentUserDict, getLoggedUserObject, CommentFull
from django.contrib import messages
from ..forms.request_forms import CreateRequestForm, AssignTechnicianForm, ServiceRCommentForm
from django.core.files.storage import FileSystemStorage

# NOTE: DONE!
def list_requests(request: HttpRequest) -> HttpResponse:
    currentUserData = getCurrentUserDict(request)
    if currentUserData == {}:
        messages.warning(request, 'You need to log in to visit this page.')
        return HttpResponseRedirect('/user/login/')

    print(currentUserData)
    if currentUserData['role'] not in ['Technician', 'Officer']:
        messages.warning(request, 'You don\'t have sufficient rights to access this page.')
        return HttpResponseRedirect('/')

    requests = ServiceRequest.objects.all()
    context = {
        'title': 'Request List',
        'requests': requests,
        'currentUserData': currentUserData,
    }

    return render(request, 'requests/list.html', context)


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
        'owner': owner,
        'comments' : fullComments,
        'commentsCount' : len(fullComments),
        'comment_form' : ServiceRCommentForm()
    }

    return render(request, 'requests/details.html', context)

# TODO:FIXME:
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
