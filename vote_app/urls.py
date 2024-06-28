from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.homepage), name='home'),
    path('about/', login_required(views.about), name='about'),
    path('account/', login_required(views.account), name='account'),
    path('create-poll/', login_required(views.create_poll), name='create_poll'),
    path('submit-poll/', login_required(views.submit_poll), name='submit_poll'),
    path('manage-elections/', login_required(views.manage_elections), name='manage_elections'),
    path('change-password/', login_required(views.change_password), name='change_password'),
    path('submit-password/', login_required(views.submit_password), name='submit_password'),
    path("index/", login_required(views.index), name="index"),  # Root URL for the app
    path("index/<int:id>/", login_required(views.index_id), name="index_id"),  # URL with an integer ID
    path("main/", login_required(views.main), name="main"),  # Additional URL for the 'main' view
    path("dashboard/", login_required(views.dashboard), name="dashboard"),  # URL for the 'dashboard' view
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('allauth.urls')),  # Include allauth URLs for authentication
]
