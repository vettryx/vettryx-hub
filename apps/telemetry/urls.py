"""
==============================================================================
Módulo: Roteamento (URLs)
Caminho: apps/telemetry/urls.py
==============================================================================
"""
from django.urls import path

from . import views

app_name = "telemetry"

urlpatterns = [
    # Rota: /api/v1/telemetry/logs/
    path("logs/", views.TelemetryLogCreateAPIView.as_view(), name="api_logs_create"),
]
