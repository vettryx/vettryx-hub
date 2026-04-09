"""
==============================================================================
Módulo: Roteamento Principal (Root URLs)
Caminho: vettryx_hub/urls.py
==============================================================================

Define as rotas principais e o acesso ao painel administrativo do VETTRYX Hub.
"""
from django.contrib import admin
from django.urls import include, path

# --- CUSTOMIZAÇÃO GLOBAL DO PAINEL ADMIN ---
admin.site.site_header = "VETTRYX Hub"
admin.site.site_title = "Admin VETTRYX"
admin.site.index_title = "Painel de Gestão Integrada"

urlpatterns = [
    # Painel Administrativo do Django
    path("admin/", admin.site.urls),

    # --- Roteamento da API RESTful ---
    path("api/v1/licenses/", include("licenses.urls")),
    path("api/v1/telemetry/", include("telemetry.urls")),
]
