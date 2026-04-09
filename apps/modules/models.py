"""
==============================================================================
Módulo: Modelos de Módulos (Modules Models)
Caminho: apps/modules/models.py
==============================================================================

Define o catálogo de soluções (plugins/módulos) da VETTRYX Tech que
poderão ser licenciados e ativados nos clientes, separados por plataforma.
"""

from common.models import AuxModuleType, AuxPlatform, IdleBase
from django.db import models
from django.utils.text import slugify


class Module(IdleBase):
    """
    Catálogo de Soluções (Módulos/Plugins/Sistemas).
    Tabela: modules
    Herda 'idle' e 'notes' de IdleBase.
    """
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Nome do Módulo"
    )
    platform = models.ForeignKey(
        AuxPlatform,
        on_delete=models.PROTECT,
        verbose_name="Plataforma Alvo"
    )
    module_type = models.ForeignKey(
        AuxModuleType,
        on_delete=models.PROTECT,
        verbose_name="Tipo de Módulo"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="Slug (Identificador Único)"
    )

    class Meta:
        verbose_name = "Módulo"
        verbose_name_plural = "Módulos"
        db_table = "modules"
        ordering = ['name']

    def save(self, *args, **kwargs):
        # Gera o slug automaticamente a partir do nome, caso esteja vazio
        if not self.slug and self.name:
            self.slug = slugify(self.name)

        # Garante que o slug sempre seja salvo em letras minúsculas
        if self.slug:
            self.slug = self.slug.lower().strip()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.platform.name}] {self.name} ({self.module_type.name})"
