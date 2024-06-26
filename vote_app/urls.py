from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('about/', views.about, name='about'),
    path('account/', views.account, name='account'),
    path('create-poll/', views.create_poll, name='create_poll'),
    path('submit-poll/', views.submit_poll, name='submit_poll'), 
    path('manage-elections/', views.manage_elections, name='manage_elections'),
    path('change-password/', views.change_password, name='change_password'),
    path('submit-password/', views.submit_password, name='submit_password'),
]