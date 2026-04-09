"""
==============================================================================
Módulo: Administração (Admin)
Caminho: apps/licenses/admin.py
==============================================================================

Registra o modelo de licenças e suas permissões no painel administrativo.
"""

from django.contrib import admin

from .models import License, LicenseModulePermission


class LicenseModulePermissionInline(admin.TabularInline):
    """Permite gerenciar as permissões (Feature Toggles) na tela da licença."""
    model = LicenseModulePermission
    extra = 1


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid",)
    list_display = ("uuid", "client", "site_url", "expiration_date", "idle")
    list_filter = ("idle", "client")
    search_fields = ("uuid", "site_url", "client__name")
    ordering = ("-expiration_date",)
    inlines = [LicenseModulePermissionInline]
