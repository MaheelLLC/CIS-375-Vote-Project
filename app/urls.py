from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup, name="signup"),
    path("login", views.login_, name="login"),
    path("logout", views.logout_, name="logout"),
    path("create", views.create, name="create"),
    path("<str:slug>/vote", views.vote, name="vote"),
    path("<str:slug>/results", views.results, name="results"),
]
