"""
==============================================================================
Módulo: Administração (Admin)
Caminho: apps/clients/admin.py
==============================================================================

Registra os modelos de clientes e contatos no painel administrativo
do Django para gerenciamento rápido via interface web.
"""

from django.contrib import admin

from .models import Client, ClientContact


class ClientContactInline(admin.TabularInline):
    """Permite cadastrar contatos na mesma tela do cadastro do cliente."""
    model = ClientContact
    extra = 1


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("uid", "name", "person_type", "cpf_cnpj", "idle")
    list_filter = ("person_type", "idle")
    search_fields = ("name", "fantasy_name", "cpf_cnpj", "uid")
    ordering = ("name",)
    inlines = [ClientContactInline]
