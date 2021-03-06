"""conf URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
from django.urls import path
from .views import (logout_view,
                    LoginFormView,
                    ElectorSinCuentaListView,
                    CuentaElectorListView,
                    ConfirmarCuenta,)

app_name = 'gest_usuario'
urlpatterns = [
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    # accounts/gen-cue-elector/
    path('gen-cue-elector/', ElectorSinCuentaListView.as_view(), name='gen-cu-elector'),
    path('cuenta-elector/', CuentaElectorListView.as_view(), name='cuenta-elector'),
    # gest_usuario:cinfirmar
    path('confirmar/', ConfirmarCuenta.as_view(), name='confirmar'),
]
