"""conf URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from django.urls import path
from . import views

app_name = 'gest_programacion'
urlpatterns = [
    path('administrar/<int:pk>/programar',
         views.AdmProgramacion.as_view(), name='adm-programar'),

]
