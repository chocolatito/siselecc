"""conf URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from django.urls import path
from . import views

app_name = 'gest_cargo'
urlpatterns = [
    path('agregar', views.CargoCreateView.as_view(), name='agregar'),
    path('listado', views.CargoListView.as_view(), name='listado'),
    path('listado/<int:pk>', views.CargoDetailView.as_view(), name='detalle'),
    path('listado/<int:pk>/actualizar', views.CargoUpdateView.as_view(), name='actualizar'),
]
