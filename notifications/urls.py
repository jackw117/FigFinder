from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('details/<int:pk>', views.details, name='details')
]