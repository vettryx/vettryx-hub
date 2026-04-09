"""
==============================================================================
Módulo: Administração (Admin)
Caminho: apps/telemetry/admin.py
==============================================================================

Registra o modelo de telemetria no painel administrativo do Django.
Configurado como "Somente Leitura" para garantir a integridade da auditoria.
"""

from django.contrib import admin

from .models import TelemetryLog


@admin.register(TelemetryLog)
class TelemetryLogAdmin(admin.ModelAdmin):
    list_display = ("level", "license", "module_slug", "created_at")
    list_filter = ("level", "created_at")
    search_fields = ("license__site_url", "module_slug", "message")
    ordering = ("-created_at",)

    # Logs são imutáveis: não podem ser adicionados manualmente nem alterados
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
