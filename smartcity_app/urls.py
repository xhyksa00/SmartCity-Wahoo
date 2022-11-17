from django.urls import path
from .Views import user_views

#URLConf
urlpatterns = [
    path('user/login/', user_views.login),
]