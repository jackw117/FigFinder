from django.urls import include, path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('register', views.register, name='register'),
    path('settings', views.settings, name='settings'),
    path('change-password', views.change_password, name='change-password'),
    path('login', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout')
]