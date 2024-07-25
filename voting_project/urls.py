"""
URL configuration for voting_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site URL
    path('vote/', include('vote_app.urls')),  # Include the vote_app URLs
    path('accounts/', include('allauth.urls')),  # Include URLs from allauth for authentication
    path('', include(tf_urls)),  # Include URLs for two-factor authentication
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),  # Password reset URL
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),  # Password reset confirm URL
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout URL
]
