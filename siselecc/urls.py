"""siselecc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
# ___________________
from django.contrib import admin
# para Django Toolbar
from .settings import DEBUG
#
from django.urls import path, include
#

urlpatterns = [
    path('', include('apps.bienvenida.urls')),
    path('accounts/', include('apps.gest_usuario.urls')),
    path('gestor-cargo/', include('apps.gest_cargo.urls')),
    path('gestor-cifrado/', include('apps.gest_cifrado.urls')),
    path('gestor-elector/', include('apps.gest_elector.urls')),
    path('gestor-preparacion/', include('apps.gest_preparacion.urls')),
    path('gestor-programacion/', include('apps.gest_programacion.urls')),
    path('gestor-votacion/', include('apps.gest_votacion.urls')),
    path('admin/', admin.site.urls),
]

if DEBUG:
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
