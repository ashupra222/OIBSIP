from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("vc/", views.videochat, name="vc"),
    path("<str:room_name>/", views.room, name="room"),
]