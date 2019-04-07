from django.urls import path
from dynamic import views

urlpatterns = [
    path("send/", views.send),
    path("list/", views.dynamic_list),
    path("photo/", views.get_photo),
    path("delete/", views.delete_dynamic),
    path("like/", views.like_dynamic),
    path("comment/", views.comment_dynamic),
    path("detail/",views.get_comment),
]
