"""conf URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from django.urls import path
from . import views

app_name = 'gest_preparacion'
urlpatterns = [
    path('agregar',
         views.EleccionCreateView.as_view(), name='agregar'),
    path('listado',
         views.EleccionListView.as_view(), name='listado'),
    path('listado/<int:pk>',
         views.EleccionDetailView.as_view(), name='detalle'),
    path('listado/<int:pk>/actualizar',
         views.EleccionUpdateView.as_view(), name='actualizar'),
    path('administrar/padron/<int:pk>',
         views.PadronDetailView.as_view(), name='adm-padron'),
    path('administrar/mesa/<int:pk>',
         views.MesaDetailView.as_view(), name='adm-mesa'),
    path('administrar/candidatos/<int:pk>',
         views.AdministrarCandidatos.as_view(), name='adm-candidato'),

]
