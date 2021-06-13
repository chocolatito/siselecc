"""conf URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from django.urls import path
from . import views

app_name = 'gest_votacion'
urlpatterns = [
    # Mesa
    path('iniciar/mesa/<int:pk>', views.IniMesa.as_view(), name='ini-mesa'),
    path('iniciar/urna', views.IniUrna.as_view(), name='ini-urna'),
    #
    path('mesa-iniciada/<int:pk>', views.MesaIni.as_view(), name='mesa-ini'),
    path('mesa-iniciada/<int:pk>/operativa', views.MesaOpe.as_view(), name='mesa-ope'),
    path('autorizar/<int:pk>',
         views.AutorizarElector.as_view(), name='autorizar'),
    #
    path('urna-operativa/<int:pk>', views.UrnaOpe.as_view(), name='urna-ope'),
    path('urna-operativa/<int:pk>/confirmar/<id_boleta>',
         views.UrnaOpe.as_view(), name='urna-confirmar'),
    # path('urna-iniciada/<int:pk>', views.UrnaIni.as_view(), name='urna-ini'),
]
