from django.urls import path
from .Views import user_views


userUrls = [
    path('user/login/', user_views.login),
    path('user/register/', user_views.register),
    ]

#URLConf
urlpatterns = userUrls