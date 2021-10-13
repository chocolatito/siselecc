"""conf URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from django.urls import path
from . import views

app_name = 'bienvenida'
urlpatterns = [
    path('', views.Bienvenida.as_view(), name='bienvenida'),
    path('proxima/<int:pk>', views.DetallesProxima.as_view(), name='proxima'),
    path('cerrada/<int:pk>', views.DetallesCerrada.as_view(), name='cerrada'),
    path('resultado/<int:pk>', views.Resultado.as_view(), name='resultado'),
]
