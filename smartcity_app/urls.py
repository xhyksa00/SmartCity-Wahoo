from django.urls import path
from .views import user_views, tickets_views


userUrls = [
    path('user/login/', user_views.login),
    path('user/register/', user_views.register),
    path('user/registerConfiramtion/', user_views.registerConfirmation)
    
    ]

ticketsUrls = [
    path('tickets/list', tickets_views.list_tickets)
]

testUrls = [
    path('hello/', user_views.sayHello)
]

#URLConf
urlpatterns = userUrls + testUrls + ticketsUrls
