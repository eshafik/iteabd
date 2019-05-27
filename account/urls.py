from django.urls import path,include
from django.conf.urls import url

from django.contrib.auth import views as auth_views
from . import views


# app_name = "account"

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', include('django.contrib.auth.urls')),

    # registration
    path('register/', views.register, name="register"),
    path('', views.dashboard, name='dashboard'),

    # profile edit
    path('edit/', views.edit, name='edit'),
    # profile details
    path('@/<slug:username>/', views.profile_details, name='profile_details'),

    path('all_members/', views.all_members, name='all_members'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]