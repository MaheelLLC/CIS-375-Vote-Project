from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', login_required(views.electionPage), name='home'),
    path('about/', login_required(views.about), name='about'),
    path('account/', login_required(views.account), name='account'),
    path('create-poll/', login_required(views.create_poll), name='create_poll'),
    path('delete_polls/', login_required(views.delete_all_polls), name='delete_polls'),
    path('submit-poll/', login_required(views.submit_poll), name='submit_poll'),
    path('electionPage/', login_required(views.electionPage), name='electionPage'),
    path('manage-elections/', login_required(views.manage_elections), name='manage_elections'),
    path('change-password/', login_required(views.change_password), name='change_password'),
    path('submit-password/', login_required(views.submit_password), name='submit_password'),
    path('index/', login_required(views.index), name='index'),  # Root URL for the app
    path('index/<int:id>/', login_required(views.index_id), name='index_id'),  # URL with an integer ID
    path('main/', login_required(views.main), name='main'),  # Additional URL for the 'main' view
    path('dashboard/', login_required(views.dashboard), name='dashboard'),  # URL for the 'dashboard' view
    path('login/', views.login_view, name='login'),  # Login URL without login required
    path('register/', views.register_view, name='register'),  # Register URL without login required
    path('accounts/', include('allauth.urls')),  # Include allauth URLs for authentication
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('<str:slug>/vote', views.vote, name='vote'),
]
