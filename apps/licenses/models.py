"""
==============================================================================
Módulo: Modelos de Licenças (Licenses Models)
Caminho: apps/licenses/models.py
==============================================================================

Define a entidade central de Licenciamento do VETTRYX Hub.
Gera e gerencia os UUIDs únicos que autorizam o funcionamento dos
plugins nos sites dos clientes, bem como suas permissões de módulos.
"""

import uuid

from clients.models import Client
from common.models import IdleBase
from django.db import models
from modules.models import Module


class License(IdleBase):
    """
    Registro de Licenças (Sites autorizados).
    Tabela: licenses
    Herda 'idle' e 'notes' de IdleBase.
    """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="UUID da Licença"
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name="licenses",
        verbose_name="Cliente"
    )
    site_url = models.URLField(
        max_length=255,
        verbose_name="URL do Site"
    )
    expiration_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Data de Expiração"
    )

    class Meta:
        verbose_name = "Licença"
        verbose_name_plural = "Licenças"
        db_table = "licenses"
        ordering = ['client', 'site_url']

    def __str__(self):
        return f"{self.site_url} - {self.client.name}"


class LicenseModulePermission(IdleBase):
    """
    Tabela Pivot (N:N): Relacionamento de permissões entre Licenças e Módulos.
    Define quais módulos (Feature Toggles) estão ativos para uma licença.
    Tabela: license_module_permission
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID da Permissão"
    )
    license = models.ForeignKey(
        License,
        on_delete=models.CASCADE,
        related_name="permissions",
        verbose_name="Licença"
    )
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="licenses_permissions",
        verbose_name="Módulo"
    )
    is_enabled = models.BooleanField(
        default=True,
        verbose_name="Habilitado?"
    )

    class Meta:
        verbose_name = "Permissão de Módulo"
        verbose_name_plural = "Permissões de Módulos"
        db_table = "license_module_permission"
        constraints = [
            models.UniqueConstraint(
                fields=['license', 'module'],
                name='unique_license_module'
            )
        ]

    def __str__(self):
        status = "Ativo" if self.is_enabled else "Inativo"
        return f"[{status}] {self.module.name} para {self.license.site_url}"
