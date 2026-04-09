"""
==============================================================================
Módulo: Serializadores (Serializers)
Caminho: apps/telemetry/serializers.py
==============================================================================

Valida e converte o payload JSON recebido da API em objetos do banco de dados.
"""

from rest_framework import serializers

from .models import TelemetryLog


class TelemetryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelemetryLog
        # A licença não vem no payload do JSON, ela vem do cabeçalho Bearer.
        # Portanto, só esperamos estes 4 campos no corpo da requisição:
        fields = ['level', 'module_slug', 'message', 'payload']
