"""
==============================================================================
Módulo: Visualizações da API (Views)
Caminho: apps/telemetry/views.py
==============================================================================

Endpoints para recebimento e processamento de telemetria.
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import TelemetryLogSerializer


class TelemetryLogCreateAPIView(APIView):
    """
    Endpoint: POST /api/v1/telemetry/logs/ (Issue #9)
    Recebe logs e erros dos sites clientes e salva no banco de dados.
    A autenticação Bearer (Licença) é garantida globalmente.
    """

    def post(self, request, *args, **kwargs):
        serializer = TelemetryLogSerializer(data=request.data)

        if serializer.is_valid():
            # Salva o log amarrando-o automaticamente à licença validada no Header
            serializer.save(license=request.auth)

            return Response(
                {"status": "success", "message": "Log registrado com sucesso."},
                status=status.HTTP_201_CREATED
            )

        # Se o JSON vier com formato errado ou faltando campos obrigatórios
        return Response(
            {"status": "error", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
