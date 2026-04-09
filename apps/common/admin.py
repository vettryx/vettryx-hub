"""
==============================================================================
Módulo: Administração (Admin)
Caminho: apps/common/admin.py
==============================================================================

Registra os modelos de domínio (tabelas auxiliares) no painel administrativo
do Django para fácil gerenciamento (CRUD) via interface web.
"""

from django.contrib import admin

from .models import AuxContactType, AuxModuleType, AuxPlatform


@admin.register(AuxContactType)
class AuxContactTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "idle", "notes")
    list_filter = ("idle",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(AuxModuleType)
class AuxModuleTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "idle", "notes")
    list_filter = ("idle",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(AuxPlatform)
class AuxPlatformAdmin(admin.ModelAdmin):
    list_display = ("name", "idle", "notes")
    list_filter = ("idle",)
    search_fields = ("name",)
    ordering = ("name",)
