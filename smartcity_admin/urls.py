from django.urls import path
from .views import login, logout, usersList, viewUser, deleteUser, changePassword

urlpatterns = [
    path('login/', login),
    path('logout/', logout),
    path('user/list/', usersList),
    path('user/<int:id>/', viewUser),
    path('user/delete/<int:id>/', deleteUser),
    path('changePassword/', changePassword),
    path('', login),
]
