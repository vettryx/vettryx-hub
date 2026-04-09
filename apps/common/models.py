"""
==============================================================================
Módulo: Modelos Comuns (Common Models)
Caminho: apps/common/models.py
==============================================================================

Este módulo contém as classes base abstratas (Mixins) e as tabelas de domínio
auxiliares que formam a fundação do banco de dados e serão herdadas por
outros aplicativos dentro do VETTRYX Hub.
"""

import re
import unicodedata

from django.db import models


class NoteBase(models.Model):
    """
    Nível 1 (Mixin): Apenas Observações.
    Fornece um campo padrão de observações livre para as tabelas filhas.
    """

    notes = models.TextField(blank=True, null=True, verbose_name="Observações")

    class Meta:
        abstract = True


class IdleBase(NoteBase):
    """
    Nível 2 (Mixin): Observações + Inativo (Idle).
    Herda 'notes' e adiciona a lógica de Soft Delete (Inativação) padrão do sistema.
    """

    SIM_NAO = [
        (False, "Não"),
        (True, "Sim"),
    ]

    idle = models.BooleanField(default=False, verbose_name="Inativo?", choices=SIM_NAO)

    class Meta:
        abstract = True


class AuxContactType(IdleBase):
    """
    Tabela Dominio: Define os meios de contato permitidos no sistema.
    Ex: E-mail, WhatsApp, Telefone Residencial, etc.
    Tabela: aux_contact_type
    """

    name = models.CharField(max_length=255, unique=True, verbose_name="Nome")

    class Meta:
        verbose_name = "Tipo de Contato"
        verbose_name_plural = "Tipos de Contatos"
        db_table = "aux_contact_type"

    def __str__(self):
        return self.name


class AuxModuleType(IdleBase):
    """
    Tabela Dominio: Categoriza os módulos da agência para controle de exibição/upsell.
    Ex: Core, Gratuito, Premium.
    Tabela: aux_modules_types
    """

    name = models.CharField(max_length=255, unique=True, verbose_name="Nome")

    class Meta:
        verbose_name = "Tipo de Módulo"
        verbose_name_plural = "Tipos de Módulos"
        db_table = "aux_modules_types"

    def __str__(self):
        return self.name


class AuxPlatform(IdleBase):
    """
    Tabela Dominio: Define as plataformas/ecossistemas atendidos.
    Ex: WordPress, Windows, Android, Web SaaS.
    Tabela: aux_platforms
    """
    name = models.CharField(max_length=255, unique=True, verbose_name="Nome")

    class Meta:
        verbose_name = "Plataforma"
        verbose_name_plural = "Plataformas"
        db_table = "aux_platforms"

    def __str__(self):
        return self.name


class ContactBase(models.Model):
    """
    Classe Abstrata (Mixin) para Contatos.
    Padroniza a limpeza e formatação automática de telefones e e-mails antes de salvar no banco.
    """

    contact_type = models.ForeignKey(
        AuxContactType, on_delete=models.PROTECT, verbose_name="Tipo de Contato"
    )
    value = models.CharField(max_length=255, verbose_name="Valor (Tel/Email)")

    class Meta:
        abstract = True

    def __str__(self):
    # Utiliza getattr para evitar erro caso a classe filha não implemente um campo 'client'
        return f"{getattr(self, 'client', 'Contato')}: {self.value}"

    def save(self, *args, **kwargs):
        if self.value:
            self.value = self.value.strip()

            # =================================================================
            # ATENÇÃO: HARDCODED IDs (Magic Numbers)
            # Estes IDs assumem que a tabela aux_contact_type será populada
            # EXATAMENTE nesta ordem no banco de dados de produção.
            # 1: Tel Resid, 2: Tel Com, 3: Cel Pessoal, 4: Cel Corp
            PHONES_BR = [1, 2, 3, 4]
            # 5: Email Pessoal, 6: Email Corporativo
            EMAILS = [5, 6]
            # 7: Telefone Exterior
            PHONE_EXT = [7]
            # =================================================================

            # Normalização de E-mails (sempre minúsculo)
            if self.contact_type_id in EMAILS:
                self.value = self.value.lower()

            # Formatação de Telefones Brasileiros (Garante DDI +55)
            elif self.contact_type_id in PHONES_BR:
                numbers = re.sub(r"[^0-9]", "", self.value)
                MAX_LENGTH_WITHOUT_COUNTRY_CODE = 11

                if len(numbers) <= MAX_LENGTH_WITHOUT_COUNTRY_CODE:
                    numbers = "55" + numbers

                self.value = f"+{numbers}"

            # Formatação de Telefones Internacionais (Apenas adiciona o '+')
            elif self.contact_type_id in PHONE_EXT:
                numbers = re.sub(r"[^0-9]", "", self.value)
                self.value = f"+{numbers}"

        super().save(*args, **kwargs)
