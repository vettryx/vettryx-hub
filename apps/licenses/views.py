"""
==============================================================================
Módulo: Visualizações e Controladores (Views)
Caminho: apps/licenses/views.py
==============================================================================

Contém a lógica de apresentação e os endpoints da API para as licenças.
"""

from modules.models import Module
from rest_framework.response import Response
from rest_framework.views import APIView


class LicenseSyncAPIView(APIView):
    """
    Endpoint: GET /api/v1/licenses/sync/ (Issue #8)

    Como configuramos a segurança globalmente no settings.py, se o código
    chegar nesta função, é 100% garantido que o token Bearer é válido e
    que a licença está ativa. O objeto da licença já estará disponível
    automaticamente dentro de `request.auth`.
    """

    def get(self, request, *args, **kwargs):
        # A licença que passou pela barreira de segurança (Bearer Token)
        license_obj = request.auth

        # 1. Busca os módulos HABILITADOS para esta licença específica
        enabled_permissions = license_obj.permissions.filter(
            is_enabled=True,
            module__idle=False
        ).select_related("module")

        modules_enabled = [
            {
                "slug": perm.module.slug,
                "name": perm.module.name,
            }
            for perm in enabled_permissions
        ]

        # 2. Busca TODOS os módulos DISPONÍVEIS no catálogo (ativos)
        # O WordPress pode usar isso para exibir um "Catálogo de Upsell" no painel do cliente
        active_modules = Module.objects.filter(idle=False)
        modules_available = [
            {
                "slug": mod.slug,
                "name": mod.name,
                "platform": mod.platform.name,
                "type": mod.module_type.name,
            }
            for mod in active_modules
        ]

        # 3. Monta o Payload JSON exato exigido pela Issue #8
        payload = {
            "license": {
                "status": "active",
                "site_url": license_obj.site_url,
                "expiration_date": license_obj.expiration_date,
            },
            "modules_enabled": modules_enabled,
            "modules_available": modules_available,
        }

        # O DRF (Response) converte esse dicionário Python em JSON automaticamente, retornando HTTP 200 OK
        return Response(payload)
