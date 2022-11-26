from django.urls import path
from .views import rootpage_view, user_views, tickets_views
from django.conf import settings
from django.conf.urls.static import static

userUrls = [
    path('user/login/', user_views.login, name='user-login'),
    path('user/register/', user_views.register, name='user-register'),
    path('user/<int:id>/', user_views.viewUser, name='user-view'),
    path('user/logout/', user_views.logout, name='user-logout'),
    path('user/edit/<int:id>/', user_views.editProfile, name='user-edit'),
    path('user/delete/<int:id>/', user_views.deleteAccount, name='user-delete'),
    path('user/edit/password/<int:id>/', user_views.changePassword, name='user-change-password'),
    path('user/list/', user_views.listUsers, name='List users')
]

ticketsUrls = [
    path('tickets/list/', tickets_views.list_tickets, name='list-tickets'),
    path('tickets/list/<int:id>/', tickets_views.show_ticket, name='ticket-details'),
    path('tickets/create/', tickets_views.create_ticket, name='create-ticket'),
    path('tickets/edit/<int:id>/', tickets_views.edit_ticket, name='edit-ticket'),
]

rootUrl = [
    path('', rootpage_view.rootPage),
]

testUrls = [
]

imageUrls = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# URLConf VVV #note: For some reason, imageUrls has to be last in this concatenation...
# ^^^ #note: Probably cause it's not an array, and python does some implicit shit
urlpatterns = userUrls + testUrls + ticketsUrls + rootUrl + imageUrls
