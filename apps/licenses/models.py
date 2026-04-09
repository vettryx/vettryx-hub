"""
==============================================================================
Módulo: Modelos de Licenças (Licenses Models)
Caminho: apps/licenses/models.py
==============================================================================

Define a entidade central de Licenciamento do VETTRYX Hub.
Gera e gerencia os UUIDs únicos que autorizam o funcionamento dos
plugins nos sites dos clientes.
"""

import uuid

from clients.models import Client
from common.models import IdleBase
from django.db import models


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
