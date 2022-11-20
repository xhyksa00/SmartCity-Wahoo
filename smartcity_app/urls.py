from django.urls import path
from .views import rootpage_view, user_views, tickets_views
from django.conf import settings
from django.conf.urls.static import static

userUrls = [
    path('user/login/', user_views.login),
    path('user/register/', user_views.register),
    path('user/<int:id>/', user_views.viewUser),
    path('user/logout/', user_views.logout),
    path('user/edit/<int:id>/', user_views.editProfile),
    path('user/delete/<int:id>/', user_views.deleteAccount),
    path('user/edit/password/<int:id>/', user_views.changePassword),
    ]

ticketsUrls = [
    path('tickets/list/', tickets_views.list_tickets, name='list-tickets'),
    path('tickets/<int:id>/', tickets_views.show_ticket, name='ticket-details'),
    #path('tickets/create', tickets_views.create_ticket, name='create-ticket'),
]

rootUrl = [
    path('',rootpage_view.rootPage), 
]

testUrls = [
]

imageUrls = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#URLConf VVV #note: For some reason, imageUrls has to be last in this concatenation...
urlpatterns = userUrls + testUrls + ticketsUrls  + rootUrl + imageUrls
