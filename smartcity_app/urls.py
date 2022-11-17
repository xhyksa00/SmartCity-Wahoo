from django.urls import path
from .Views import user_views


userUrls = [
    path('user/login/', user_views.login),
    path('user/register/', user_views.register),
    path('user/registerConfiramtion/', user_views.registerConfirmation)
    
    ]

testUrls = [
    path('hello/', user_views.sayHello)
]

#URLConf
urlpatterns = userUrls + testUrls