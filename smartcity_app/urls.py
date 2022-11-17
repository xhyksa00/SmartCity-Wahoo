from django.urls import path
from . import views

#URLConf
urlpatterns = [
    path('login/', views.login),
]