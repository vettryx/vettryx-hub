"""
==============================================================================
Módulo: Administração (Admin)
Caminho: apps/modules/admin.py
==============================================================================
"""

from django.contrib import admin

from .models import Module


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("name", "platform", "module_type", "slug", "idle")
    list_filter = ("platform", "module_type", "idle")
    search_fields = ("name", "slug")
    ordering = ("platform", "name")

    # Preenche o slug automaticamente enquanto você digita o nome
    prepopulated_fields = {"slug": ("name",)}
