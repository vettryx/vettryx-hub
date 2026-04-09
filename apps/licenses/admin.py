"""
==============================================================================
Módulo: Administração (Admin)
Caminho: apps/licenses/admin.py
==============================================================================

Registra o modelo de licenças e suas permissões no painel administrativo.
Adiciona ações customizadas para gestão do ciclo de vida das chaves de API.
"""

import uuid

from django.contrib import admin, messages
from django.utils.translation import ngettext

from .models import License, LicenseModulePermission


# --- AÇÕES CUSTOMIZADAS (Issue #11) ---
@admin.action(description="Gerar Nova Chave de API (Revogar Atual)")
def generate_new_api_key(modeladmin, request, queryset):
    """
    Gera um novo UUID para as licenças selecionadas, efetivamente
    revogando o acesso da chave antiga.
    """
    updated_count = 0
    for license_obj in queryset:
        license_obj.uuid = uuid.uuid4()
        license_obj.save()
        updated_count += 1

    # Feedback visual verde no painel após a ação
    modeladmin.message_user(
        request,
        ngettext(
            'Nova chave de API gerada com sucesso para %d licença.',
            'Novas chaves de API geradas com sucesso para %d licenças.',
            updated_count,
        ) % updated_count,
        messages.SUCCESS,
    )


# --- CONFIGURAÇÃO VISUAL DO PAINEL ---
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
    actions = [generate_new_api_key]
