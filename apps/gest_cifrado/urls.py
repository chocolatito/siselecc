"""conf URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from django.urls import path
from . import views

app_name = 'gest_cifrado'
urlpatterns = [
    path('', views.GestorCifradoView.as_view(), name='gest_cifrado'),
    path('inicializar/publica/<int:pk>',
         views.IniPublica_I.as_view(), name='ini-publica-i'),
    path('inicializar/publica/<int:pk>/ingreso-clave',
         views.IniPublica_II.as_view(), name='ini-publica-ii'),
    path('inicializar/privada/<int:pk>',
         views.IniPrivada_I.as_view(), name='ini-privada-i'),
    path('iniciar/conteo/<int:pk>', views.IniConteo.as_view(), name='ini-conteo'),
    # path('inicializar/elecciones', views.EleccionesProgramadas.as_view(), name='ini-elecciones'),
    #path('inicializar/privada', views.CargoListView.as_view(), name='ini-privada'),
]
