"""
==============================================================================
Módulo: Configuração do App (App Config)
Caminho: apps/licenses/apps.py
==============================================================================

Arquivo de configuração central do aplicativo 'licenses'.
Define o nome, o campo de ID padrão e como ele aparece no painel admin.
"""

from django.apps import AppConfig


class LicensesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "licenses"
    verbose_name = "Gestão de Licenças"
