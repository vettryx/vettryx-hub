"""
==============================================================================
Módulo: Roteamento Principal (Root URLs)
Caminho: vettryx_hub/urls.py
==============================================================================

Define as rotas principais e o acesso ao painel administrativo do VETTRYX Hub.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Painel Administrativo do Django
    path("admin/", admin.site.urls),

    # --- Roteamento da API RESTful ---
    # Qualquer requisição para /api/v1/licenses/ será tratada pelo app 'licenses'
    path("api/v1/licenses/", include("licenses.urls")),
]
