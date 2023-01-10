from . import views
from django.urls import path

urlpatterns = [
    path("<str:id>", views.index, name = "index"),
    path("", views.home, name = ""),
]
