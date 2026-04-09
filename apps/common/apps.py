"""
==============================================================================
Módulo: Configuração do App (App Config)
Caminho: apps/common/apps.py
==============================================================================

Arquivo de configuração central do aplicativo 'common'.
Define o nome, o campo de ID padrão e como ele aparece no painel admin.
"""

from django.apps import AppConfig


class CommonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "common"
    verbose_name = "Núcleo Comum (Domínios)"
