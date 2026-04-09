"""
==============================================================================
Módulo: Segurança da API (API Security)
Caminho: apps/common/api_security.py
==============================================================================

Mecanismos customizados de autenticação e permissão para o Django REST Framework.
Garante que os endpoints da API só sejam acessados por clientes com licenças ativas.
"""

from django.core.exceptions import ValidationError
from licenses.models import License
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission

# Expected number of parts in Authorization header: 'Bearer' + token
EXPECTED_AUTH_PARTS = 2


class BearerLicenseAuthentication(BaseAuthentication):
    """
    Autenticação customizada via Header (Issue #7).
    Formato esperado: 'Authorization: Bearer <uuid_da_licenca>'
    Retorna HTTP 401 (Unauthorized) caso falhe.
    """

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        # Se não enviou o header, recusa a autenticação
        if not auth_header:
            return None

        parts = auth_header.split()

        # Verifica se começa com 'Bearer'
        if parts[0].lower() != 'bearer':
            return None

        # Garante que tenha exatamente 2 partes: a palavra Bearer e o Token
        if len(parts) != EXPECTED_AUTH_PARTS:
            raise AuthenticationFailed('Cabeçalho Authorization inválido. Use "Bearer <token>".')

        token = parts[1]

        try:
            # Busca a licença no banco e verifica se ela NÃO está inativa (idle=False)
            license_obj = License.objects.get(uuid=token, idle=False)
        except (License.DoesNotExist, ValidationError, ValueError):
            raise AuthenticationFailed(
                "Chave de API inválida, revogada ou licença inativa."
            ) from None

        # Em APIs Machine-to-Machine, retornamos (None, objeto_de_auth).
        # Assim, nas views da API, usaremos `request.auth` para saber qual licença está acessando.
        return (None, license_obj)

    def authenticate_header(self, request):
        """
        Obrigatório no DRF para garantir o retorno HTTP 401 (Unauthorized)
        em vez de 403 (Forbidden) quando a autenticação falhar.
        """
        return 'Bearer'


class HasValidLicensePermission(BasePermission):
    """
    Permissão que exige que a requisição tenha passado com sucesso
    pela BearerLicenseAuthentication.
    """
    def has_permission(self, request, view):
        # request.auth foi populado no sucesso do método authenticate() acima
        return bool(request.auth and isinstance(request.auth, License))
