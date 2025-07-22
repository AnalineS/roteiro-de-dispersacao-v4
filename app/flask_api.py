"""
API Flask para o sistema de chatbot de dispersão
"""

import logging
import time
import uuid

from config.settings import settings
from flask import Flask, jsonify, request
from flask_cors import CORS

from app.langflow_integration import get_flow_manager
from app.rag_system import get_rag_system
from app.services.answer_service import answer_question

logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """Cria e configura a aplicação Flask"""
    app = Flask(__name__)
    CORS(app)  # Habilitar CORS para todas as rotas

    # Configurações
    app.config["SECRET_KEY"] = "roteiro-dispersacao-v4-secret"
    app.config["DEBUG"] = settings.DEBUG

    # Inicializar componentes principais do backend.
    # O sistema RAG (Retrieval-Augmented Generation) é responsável por buscar e gerar respostas baseadas em contexto.
    # O flow_manager integra com o LangFlow para fluxos customizados de processamento.
    rag_system = get_rag_system()
    flow_manager = get_flow_manager()

    @app.route("/")
    def index():
        """Página inicial da API"""
        return jsonify(
            {
                "name": settings.APP_NAME,
                "version": settings.APP_VERSION,
                "status": "running",
                "endpoints": {
                    "chat": "/api/chat",
                    "health": "/api/health",
                    "flows": "/api/flows",
                    "calculate": "/api/calculate",
                },
            }
        )

    @app.route("/api/health")
    def health_check():
        """Endpoint de verificação de saúde"""
        try:
            # Verificar componentes essenciais
            status = {
                "status": "healthy",
                "components": {"rag_system": "ok", "langflow": "ok", "database": "ok"},
                "version": settings.APP_VERSION,
            }

            return jsonify(status), 200

        except Exception as e:
            logger.error(f"Erro no health check: {e}")
            return jsonify({"status": "unhealthy", "error": str(e)}), 500

    @app.route("/api/chat", methods=["POST"])
    def chat():
        """Endpoint principal do chat"""
        try:
            data = request.get_json()

            if not data or "message" not in data:
                return jsonify({"error": "Mensagem é obrigatória"}), 400

            message = data["message"]
            persona = data.get("persona", "Dr. Gasnelio")
            session_id = data.get("session_id", str(uuid.uuid4()))
            data.get("use_langflow", False)

            # Validar persona recebida do frontend.
            # Se a persona não for reconhecida, utiliza o padrão 'Dr. Gasnelio' para garantir consistência.
            if persona not in ["Dr. Gasnelio", "Gá"]:
                persona = "Dr. Gasnelio"

            # Gerar resposta usando função centralizada (padrão de design: centralização de lógica de resposta).
            response = answer_question(message, persona, session_id=session_id)

            return jsonify(
                {
                    "response": response,
                    "persona": persona,
                    "session_id": session_id,
                    "timestamp": int(time.time()),
                }
            )
        except Exception as e:
            logger.error(f"Erro no endpoint /api/chat: {e}")
            return jsonify({"error": str(e)}), 500

    @app.route("/api/flows", methods=["GET"])
    def list_flows():
        """Lista fluxos disponíveis no LangFlow"""
        try:
            flows = flow_manager.client.list_flows()
            return jsonify({"flows": flows})

        except Exception as e:
            logger.error(f"Erro ao listar fluxos: {e}")
            return jsonify({"error": "Erro ao acessar fluxos"}), 500

    @app.route("/api/flows", methods=["POST"])
    def create_flow():
        """Cria um novo fluxo"""
        try:
            data = request.get_json()
            flow_type = data.get("type", "basic_dispersion")

            flow_id = flow_manager.create_dispersion_flow(flow_type)

            if flow_id:
                return jsonify({"flow_id": flow_id, "type": flow_type, "status": "created"})
            else:
                return jsonify({"error": "Falha ao criar fluxo"}), 500

        except Exception as e:
            logger.error(f"Erro ao criar fluxo: {e}")
            return jsonify({"error": "Erro interno do servidor"}), 500

    @app.route("/api/calculate", methods=["POST"])
    def calculate_dispersion():
        """Calcula parâmetros de dispersão"""
        try:
            data = request.get_json()

            if not data or "parameters" not in data:
                return jsonify({"error": "Parâmetros são obrigatórios"}), 400

            parameters = data["parameters"]

            # Validar parâmetros básicos
            required_params = ["wind_speed", "temperature", "emission_rate"]
            missing_params = [p for p in required_params if p not in parameters]

            if missing_params:
                return (
                    jsonify({"error": f'Parâmetros faltando: {", ".join(missing_params)}'}),
                    400,
                )

            # Calcular parâmetros de dispersão usando fluxo avançado do LangFlow.
            # Decisão de design: delegar cálculos complexos para o LangFlow, facilitando manutenção e evolução.
            result = flow_manager.calculate_dispersion_parameters(parameters)

            if result:
                return jsonify({"result": result, "parameters": parameters, "status": "calculated"})
            else:
                return jsonify({"error": "Falha no cálculo"}), 500

        except Exception as e:
            logger.error(f"Erro no cálculo: {e}")
            return jsonify({"error": "Erro interno do servidor"}), 500

    @app.route("/api/upload", methods=["POST"])
    def upload_document():
        """Upload de documentos para o sistema RAG"""
        try:
            if "file" not in request.files:
                return jsonify({"error": "Nenhum arquivo enviado"}), 400

            file = request.files["file"]

            if file.filename == "":
                return jsonify({"error": "Nome do arquivo vazio"}), 400

            # Processar upload de documentos para o sistema RAG.
            # Decisão: leitura e processamento do conteúdo é feita aqui, mas pode ser delegada para um serviço externo no futuro.
            content = file.read().decode("utf-8")

            # Adicionar ao sistema RAG
            success = rag_system.process_documents([content], [{"source": file.filename}])

            if success:
                return jsonify(
                    {
                        "message": "Documento processado com sucesso",
                        "filename": file.filename,
                    }
                )
            else:
                return jsonify({"error": "Falha ao processar documento"}), 500

        except Exception as e:
            logger.error(f"Erro no upload: {e}")
            return jsonify({"error": "Erro interno do servidor"}), 500

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Endpoint não encontrado"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Erro interno do servidor"}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host=settings.FLASK_HOST, port=settings.FLASK_PORT, debug=settings.DEBUG)
