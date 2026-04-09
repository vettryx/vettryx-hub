"""
==============================================================================
Módulo: Roteamento Principal (Root URLs)
Caminho: vettryx_hub/urls.py
==============================================================================

Define as rotas principais e o acesso ao painel administrativo do VETTRYX Hub.
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    # Painel Administrativo do Django
    path("admin/", admin.site.urls),
]
