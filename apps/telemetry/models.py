"""
==============================================================================
Módulo: Modelos de Telemetria (Telemetry Models)
Caminho: apps/telemetry/models.py
==============================================================================

Armazena os logs, erros críticos e auditorias enviadas remotamente
pelos sites dos clientes via API.
"""

from django.db import models
from licenses.models import License


class TelemetryLog(models.Model):
    """
    Registro de eventos e erros disparados pelos plugins (Issue #9).
    Tabela: telemetry_logs
    """
    LOG_LEVELS = [
        ('INFO', 'Informação'),
        ('WARN', 'Aviso'),
        ('ERR', 'Erro Crítico'),
        ('AUDIT', 'Auditoria/Segurança'),
    ]

    # Vincula o log à licença automaticamente
    license = models.ForeignKey(
        License,
        on_delete=models.CASCADE,
        related_name="telemetry_logs",
        verbose_name="Licença"
    )
    level = models.CharField(
        max_length=5,
        choices=LOG_LEVELS,
        default='INFO',
        verbose_name="Nível do Log"
    )
    module_slug = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Slug do Módulo"
    )
    message = models.TextField(
        verbose_name="Mensagem / Descrição"
    )
    # Permite salvar qualquer JSON (Tracebacks de erro do PHP, dados do servidor, etc.)
    payload = models.JSONField(
        blank=True,
        null=True,
        verbose_name="Dados Extras (JSON)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data/Hora"
    )

    class Meta:
        verbose_name = "Log de Telemetria"
        verbose_name_plural = "Logs de Telemetria"
        db_table = "telemetry_logs"
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.level}] {self.license.site_url} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"
