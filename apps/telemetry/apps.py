"""
==============================================================================
Módulo: Configuração do App (App Config)
Caminho: apps/telemetry/apps.py
==============================================================================

Arquivo de configuração central do aplicativo 'telemetry'.
Define o nome e como ele aparece no painel administrativo.
"""

from django.apps import AppConfig


class TelemetryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "telemetry"
    verbose_name = "Telemetria e Logs"
