"""
Arquivo principal da aplicação - Roteiro de Dispersão Bot v4
"""

import logging
import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path para garantir que todos os módulos do projeto possam ser importados corretamente.
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from config.settings import settings

from app.database import get_db_connection
from app.langflow_integration import get_flow_manager
from app.rag_system import get_rag_system

# Configurar logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("app.log")],
)

logger = logging.getLogger(__name__)


def initialize_application():
    """Inicializa todos os componentes da aplicação"""
    try:
        logger.info("Inicializando aplicação...")

        # Verificar variáveis de ambiente essenciais para funcionamento do sistema.
        # Decisão de design: falhar explicitamente se faltar alguma variável crítica, evitando erros silenciosos.
        required_vars = ["ASTRA_DB_TOKEN", "OPENROUTER_API_KEY", "LANGFLOW_API_KEY"]

        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)

        if missing_vars:
            raise ValueError(f"Variáveis de ambiente faltando: {', '.join(missing_vars)}")

        # Inicializar conexão com banco, sistema RAG e gerenciador de fluxos.
        # Cada componente é inicializado separadamente para facilitar manutenção e testes.
        logger.info("Inicializando conexão com Astra DB...")
        db_connection = get_db_connection()

        logger.info("Inicializando sistema RAG...")
        rag_system = get_rag_system()

        logger.info("Inicializando LangFlow...")
        flow_manager = get_flow_manager()

        logger.info("Aplicação inicializada com sucesso!")

        return {
            "db_connection": db_connection,
            "rag_system": rag_system,
            "flow_manager": flow_manager,
        }

    except Exception as e:
        logger.error(f"Erro na inicialização: {e}")
        raise


def run_streamlit():
    """Executa a aplicação Streamlit"""
    try:
        # Inicializar aplicação
        initialize_application()

        # Executar Streamlit
        import sys

        import streamlit.web.cli as stcli

        # Configurar argumentos para o Streamlit
        sys.argv = [
            "streamlit",
            "run",
            str(root_dir / "app" / "streamlit_app.py"),
            "--server.port",
            str(settings.STREAMLIT_PORT),
            "--server.address",
            settings.STREAMLIT_HOST,
            "--server.headless",
            "true",
        ]

        stcli.main()

    except Exception as e:
        logger.error(f"Erro ao executar Streamlit: {e}")
        raise


def run_flask_api():
    """Executa a API Flask"""
    try:
        from app.flask_api import create_app

        # Inicializar aplicação
        initialize_application()

        # Criar e executar app Flask
        app = create_app()
        app.run(host=settings.FLASK_HOST, port=settings.FLASK_PORT, debug=settings.DEBUG)

    except Exception as e:
        logger.error(f"Erro ao executar Flask: {e}")
        raise


def main():
    """Função principal"""
    import argparse

    # Escolha do modo de execução via linha de comando.
    # Permite rodar a aplicação como API Flask, interface Streamlit ou apenas inicializar componentes.
    parser = argparse.ArgumentParser(description="Roteiro de Dispersão Bot v4")
    parser.add_argument(
        "--mode",
        choices=["streamlit", "flask", "init"],
        default="streamlit",
        help="Modo de execução da aplicação",
    )

    args = parser.parse_args()

    try:
        if args.mode == "streamlit":
            logger.info("Iniciando aplicação Streamlit...")
            run_streamlit()
        elif args.mode == "flask":
            logger.info("Iniciando API Flask...")
            run_flask_api()
        elif args.mode == "init":
            logger.info("Inicializando componentes...")
            initialize_application()
            logger.info("Inicialização concluída com sucesso!")

    except KeyboardInterrupt:
        logger.info("Aplicação interrompida pelo usuário")
    except Exception as e:
        logger.error(f"Erro na execução: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
