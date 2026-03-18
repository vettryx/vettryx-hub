#!/usr/bin/env python3
# update_packages.py

"""
Atualiza as dependências do projeto VETTRYX Hub usando Poetry, com uma
abordagem segura e informativa.

- Verifica se o Poetry está instalado e acessível.
- Simula a atualização para mostrar o que seria atualizado sem aplicar mudanças.
- Permite ao usuário decidir se deseja prosseguir com a atualização real.
- Gera um requirements.txt usando o pip do ambiente virtual (inclui dev).
- Fornece mensagens claras e tratamento de erros robusto.

Nota: Execute no ambiente virtual do projeto para garantir que as
dependências de desenvolvimento estejam instaladas e refletidas no
requirements.txt gerado.
"""

from __future__ import annotations

import shlex
import shutil
import subprocess
import sys
from pathlib import Path

REQUIREMENTS_FILE = Path("requirements.txt")


def get_poetry_executable() -> str:
    """
    Obtém o caminho absoluto do executável do Poetry.

    Retorna:
        str: Caminho do executável do Poetry.

    Encerra o programa com código 1 se não for encontrado.
    """
    path = shutil.which("poetry")
    if path is None:
        print("Erro crítico: 'poetry' não encontrado no PATH.")
        sys.exit(1)
    return path


def run_poetry_command(executable: str, args: list[str], check: bool = True) -> str:
    """
    Executa um comando do Poetry de forma encapsulada.

    Args:
        executable: Caminho para o executável do Poetry.
        args: Lista de argumentos a serem passados ao Poetry.
        check: Se True, levanta exceção em retorno diferente de zero.

    Retorna:
        str: Saída padrão (stdout) do comando.

    Encerra o programa com código 1 em erro quando check=True.
    """
    try:
        result = subprocess.run(
            [executable, *args],
            capture_output=True,
            text=True,
            check=check,
            shell=False,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        cmd_str = shlex.join([executable, *args])
        print(f"Erro ao executar comando: {cmd_str}")
        # Mostra stderr quando disponível; fallback para stdout
        details = e.stderr or e.stdout or ""
        if details:
            print(f"Detalhes:\n{details}")
        sys.exit(1)


def export_requirements(path: Path = REQUIREMENTS_FILE) -> None:
    """
    Gera o requirements.txt usando o pip do ambiente virtual atual.

    Args:
        path: Caminho do arquivo de saída (padrão: REQUIREMENTS_FILE).
    """
    try:
        with path.open("w", encoding="utf-8") as f:
            # sys.executable garante o Python do ambiente virtual atual.
            subprocess.run(
                [sys.executable, "-m", "pip", "freeze"],
                stdout=f,
                check=True,
            )
    except Exception as e:
        print(f"Erro crítico ao gerar {path.name}: {e}")
        sys.exit(1)


def update_packages() -> None:
    """
    Executa o fluxo de simular e (opcionalmente) aplicar updates via Poetry,
    e regenera o requirements.txt.
    """
    print("--- Verificando dependências do projeto VETTRYX Hub ---")

    poetry_exe = get_poetry_executable()

    print("Simulando atualização para verificar viabilidade...")
    simulation_output = run_poetry_command(
        poetry_exe, ["update", "--dry-run"], check=False
    )

    if (
        "No dependencies to install or update" in simulation_output
        or "0 installs, 0 updates" in simulation_output
    ):
        print("\nTudo limpo! Nenhuma atualização pendente.")
        print("Regenerando requirements.txt para garantir integridade...")
        export_requirements()
        print("Processo concluído.")
        return

    print("\nAtualizações disponíveis e viáveis encontradas:")
    print(simulation_output.strip())
    print("-" * 40)

    confirm = input("Deseja aplicar essas atualizações? (s/n): ").strip().lower()
    if confirm != "s":
        print("Cancelado.")
        return

    print("\nIniciando atualização real...")
    run_poetry_command(poetry_exe, ["update"])

    print("\nRegenerando requirements.txt (incluindo desenvolvimento)...")
    export_requirements()

    print("\nProcesso concluído com sucesso!")


if __name__ == "__main__":
    update_packages()
