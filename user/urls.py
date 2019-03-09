from django.urls import path
from user import views

urlpatterns = [
    path("register/", views.register),
    path("login/", views.login),
    path("upload_avatar/", views.upload_avatar),
    path("get_avatar/", views.get_avatar),
]
