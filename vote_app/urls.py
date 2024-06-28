from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),  # Root URL redirects to homepage
    path('about/', views.about, name='about'),
    path('account/', views.account, name='account'),
    path('create-poll/', views.create_poll, name='create_poll'),
    path('submit-poll/', views.submit_poll, name='submit_poll'),
    path('manage-elections/', views.manage_elections, name='manage_elections'),
    path('change-password/', views.change_password, name='change_password'),
    path('submit-password/', views.submit_password, name='submit_password'),
    path('signup/', views.signup, name='signup'),
    path('<int:id>/', views.index_id, name='index_id'),  # URL with an integer ID
    path('main/', views.main, name='main'),  # Additional URL for the 'main' view
    path('dashboard/', views.dashboard, name='dashboard'),  # URL for the 'dashboard' view
]
