from django.urls import path
from .views import user_views, tickets_views
from django.conf import settings
from django.conf.urls.static import static

userUrls = [
    path('user/login/', user_views.login),
    path('user/register/', user_views.register),
    path('user/<int:id>/', user_views.viewUser)
    ]

ticketsUrls = [
    path('tickets/list', tickets_views.list_tickets, name='list-tickets'),
    path('tickets/<int:id>/', tickets_views.show_ticket, name='ticket-details')
]

testUrls = [
]

imageUrls = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#URLConf
urlpatterns = userUrls + testUrls + ticketsUrls + imageUrls
