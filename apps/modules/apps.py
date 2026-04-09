"""
==============================================================================
Módulo: Configuração do App (App Config)
Caminho: apps/modules/apps.py
==============================================================================

Arquivo de configuração central do aplicativo 'modules'.
Define o nome, o campo de ID padrão e como ele aparece no painel admin.
"""

from django.apps import AppConfig


class ModulesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules"
    verbose_name = "Catálogo de Soluções"
