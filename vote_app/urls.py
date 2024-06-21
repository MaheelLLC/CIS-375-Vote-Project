# vote_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:id>", views.index_id, name="index_id"),
]
