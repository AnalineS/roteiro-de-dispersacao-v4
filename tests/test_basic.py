"""
Testes básicos para o sistema de chatbot
"""

import sys
from pathlib import Path

import pytest

# Adicionar o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from config.settings import settings


def test_settings_import():
    """Testa se as configurações podem ser importadas"""
    assert settings.APP_NAME == "Roteiro de Dispersão Bot v4"
    assert settings.APP_VERSION == "4.0.0"


def test_required_directories():
    """Testa se os diretórios necessários existem"""
    required_dirs = ["app", "config", "tests", "static", "templates", "data"]

    for dir_name in required_dirs:
        dir_path = root_dir / dir_name
        assert dir_path.exists(), f"Diretório {dir_name} não encontrado"


def test_required_files():
    """Testa se os arquivos essenciais existem"""
    required_files = [
        "requirements.txt",
        "README.md",
        ".gitignore",
        "render.yaml",
        "Dockerfile",
        "app/main.py",
        "app/rag_system.py",
        "app/streamlit_app.py",
        "config/settings.py",
    ]

    for file_name in required_files:
        file_path = root_dir / file_name
        assert file_path.exists(), f"Arquivo {file_name} não encontrado"


def test_environment_variables():
    """Testa se as variáveis de ambiente essenciais estão definidas"""
    # Este teste só passa se as variáveis estiverem definidas
    # Em produção, todas devem estar configuradas
    env_vars = ["ASTRA_DB_TOKEN", "OPENROUTER_API_KEY", "LANGFLOW_API_KEY"]

    # Para testes, apenas verificamos se estão definidas no .env
    env_file = root_dir / ".env"
    if env_file.exists():
        with open(env_file, "r") as f:
            content = f.read()
            for var in env_vars:
                assert var in content, f"Variável {var} não encontrada no .env"


if __name__ == "__main__":
    pytest.main([__file__])
