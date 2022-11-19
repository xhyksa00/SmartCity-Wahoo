from django.urls import path
from .views import user_views, tickets_views


userUrls = [
    path('user/login/', user_views.login),
    path('user/register/', user_views.register),
    path('user/<int:id>/', user_views.viewUser),
    path('user/logout/', user_views.logout)
    ]

ticketsUrls = [
    path('tickets/list', tickets_views.list_tickets)
]

testUrls = [
]

#URLConf
urlpatterns = userUrls + testUrls + ticketsUrls
