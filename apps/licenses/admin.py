"""
==============================================================================
Módulo: Administração (Admin)
Caminho: apps/licenses/admin.py
==============================================================================

Registra o modelo de licenças no painel administrativo do Django.
"""

from django.contrib import admin

from .models import License


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    # O 'readonly_fields' impede que o UUID seja alterado acidentalmente
    readonly_fields = ("uuid",)
    list_display = ("uuid", "client", "site_url", "expiration_date", "idle")
    list_filter = ("idle", "client")
    search_fields = ("uuid", "site_url", "client__name")
    ordering = ("-expiration_date",)
