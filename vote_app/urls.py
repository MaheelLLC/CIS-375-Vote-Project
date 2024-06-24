# vote_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),  # Root URL for the app
    path("<int:id>", views.index_id, name="index_id"),  # URL with an integer ID
    path("main/", views.main, name="main"),  # Additional URL for the 'main' view
    path("dashboard/", views.dashboard, name="dashboard"),  # URL for the 'dashboard' view
    path("about/", views.about, name="about"),  # URL for the 'about' view
    path('signup/', views.signup, name='signup'),
]
