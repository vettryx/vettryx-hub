"""
==============================================================================
Módulo: Roteamento (URLs)
Caminho: apps/licenses/urls.py
==============================================================================

Define as rotas (endpoints) específicas do gerenciamento de licenças.
"""

from django.urls import path

from . import views

app_name = "licenses"

urlpatterns = [
    # Rota da API RESTful (Issue #8)
    path("sync/", views.LicenseSyncAPIView.as_view(), name="api_sync"),
]
