"""
Sistema RAG (Retrieval-Augmented Generation) para o chatbot
"""

import logging
from typing import Any, Dict, List

import faiss
import openai
from config.settings import settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

from app.database import get_db_connection

logger = logging.getLogger(__name__)


class RAGSystem:
    """Sistema RAG para busca e geração de respostas"""

    # Decisão de design: centralizar toda a lógica de busca, chunking, embeddings e geração de resposta nesta classe.
    # Facilita manutenção, testes e futuras extensões (ex: troca de modelo ou indexador).

    def __init__(self):
        self.embedding_model = None
        self.faiss_index = None
        self.document_store = []
        self.db_connection = get_db_connection()
        self._initialize_models()

    def _initialize_models(self):
        """Inicializa modelos de embedding e configurações"""
        try:
            # Inicializar modelo de embedding (SentenceTransformer)
            # Decisão: uso de modelo configurável via settings para flexibilidade.
            self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)

            # Configurar cliente OpenAI para OpenRouter
            # Justificativa: permite uso de LLMs externos para geração de resposta.
            openai.api_key = settings.OPENROUTER_API_KEY
            openai.api_base = settings.OPENROUTER_BASE_URL

            # Inicializar índice FAISS para busca vetorial eficiente.
            # Decisão: Inner Product (IP) para similaridade, compatível com embeddings normalizados.
            embedding_dim = self.embedding_model.get_sentence_embedding_dimension()
            self.faiss_index = faiss.IndexFlatIP(embedding_dim)

            logger.info("Modelos RAG inicializados com sucesso")

        except Exception as e:
            logger.error(f"Erro ao inicializar modelos RAG: {e}")
            raise

    def process_documents(self, documents: List[str], metadata_list: List[Dict] = None) -> bool:
        """Processa documentos e adiciona ao índice FAISS"""
        try:
            if metadata_list is None:
                metadata_list = [{}] * len(documents)

            # Dividir documentos em chunks para melhor granularidade na busca.
            # Decisão: usar RecursiveCharacterTextSplitter para garantir que chunks não quebrem frases importantes.
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP,
                length_function=len,
            )

            all_chunks = []
            all_metadata = []

            for doc, metadata in zip(documents, metadata_list):
                chunks = text_splitter.split_text(doc)
                for i, chunk in enumerate(chunks):
                    all_chunks.append(chunk)
                    chunk_metadata = metadata.copy()
                    chunk_metadata["chunk_index"] = i
                    all_metadata.append(chunk_metadata)

            # Gerar embeddings para todos os chunks.
            embeddings = self.embedding_model.encode(all_chunks)

            # Adicionar ao índice FAISS para busca vetorial.
            self.faiss_index.add(embeddings.astype("float32"))

            # Armazenar chunks e metadados localmente e no banco de dados.
            # Decisão: manter histórico local para performance e persistir no banco para resiliência.
            for chunk, embedding, metadata in zip(all_chunks, embeddings, all_metadata):
                chunk_id = f"chunk_{len(self.document_store)}"
                self.document_store.append({"id": chunk_id, "content": chunk, "metadata": metadata})

                # Salvar no banco de dados (Astra DB)
                self.db_connection.save_document_chunk(
                    chunk_id=chunk_id,
                    content=chunk,
                    embedding=embedding.tolist(),
                    metadata=metadata,
                )

            logger.info(f"Processados {len(all_chunks)} chunks de {len(documents)} documentos")
            return True

        except Exception as e:
            logger.error(f"Erro ao processar documentos: {e}")
            return False

    def search_relevant_chunks(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """Busca chunks relevantes para uma query"""
        try:
            if self.faiss_index.ntotal == 0:
                logger.warning("Índice FAISS vazio")
                return []

            # Gerar embedding da query para busca vetorial.
            query_embedding = self.embedding_model.encode([query])

            # Buscar no índice FAISS os k chunks mais similares.
            scores, indices = self.faiss_index.search(query_embedding.astype("float32"), k)

            # Recuperar chunks relevantes
            relevant_chunks = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(self.document_store):
                    chunk = self.document_store[idx].copy()
                    chunk["similarity_score"] = float(score)
                    relevant_chunks.append(chunk)

            return relevant_chunks

        except Exception as e:
            logger.error(f"Erro na busca de chunks: {e}")
            return []

    def generate_response(
        self, query: str, persona: str = "Dr. Gasnelio", session_id: str = None
    ) -> str:
        """Gera resposta usando RAG"""
        try:
            # Buscar chunks relevantes para compor o contexto da resposta.
            relevant_chunks = self.search_relevant_chunks(query, k=3)

            # Construir contexto concatenando os chunks mais relevantes.
            context = ""
            if relevant_chunks:
                context = "\n\n".join([chunk["content"] for chunk in relevant_chunks])

            # Definir prompt da persona (técnica ou amigável).
            # Decisão: prompts customizados para cada persona, facilitando adaptação do tom da resposta.
            persona_prompts = {
                "Dr. Gasnelio": """Você é o Dr. Gasnelio, um especialista técnico em roteiro de dispersão. 
                Responda de forma técnica, precisa e profissional, usando terminologia específica da área.""",
                "Gá": """Você é Gá, um assistente amigável que explica roteiro de dispersão de forma simples e acessível. 
                Use linguagem coloquial e exemplos práticos para facilitar o entendimento.""",
            }

            system_prompt = persona_prompts.get(persona, persona_prompts["Dr. Gasnelio"])

            # Construir prompt final para o LLM.
            prompt = f"""
{system_prompt}

Contexto relevante:
{context}

Pergunta do usuário: {query}

Responda baseando-se no contexto fornecido. Se o contexto não contiver informações suficientes, 
indique isso claramente e forneça uma resposta geral sobre o tópico.
"""

            # Gerar resposta via OpenRouter (LLM externo).
            response = openai.ChatCompletion.create(
                model=settings.DEFAULT_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE,
            )

            answer = response.choices[0].message.content

            # Salvar no histórico se session_id fornecido.
            # Decisão: persistir interações para auditoria e melhoria contínua.
            if session_id:
                self.db_connection.save_chat_message(
                    session_id=session_id,
                    message=query,
                    response=answer,
                    persona=persona,
                )

            return answer

        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {e}")
            return "Desculpe, ocorreu um erro ao processar sua pergunta. Tente novamente."

    def load_default_documents(self):
        """Carrega documentos padrão sobre roteiro de dispersão"""
        try:
            # Documentos básicos sobre roteiro de dispersão
            default_docs = [
                """
                Roteiro de Dispersão é um procedimento técnico utilizado em engenharia química e ambiental 
                para modelar como substâncias se espalham no ambiente após um vazamento ou liberação acidental. 
                Este processo é fundamental para avaliação de riscos e planejamento de emergências.
                
                Os principais fatores que influenciam a dispersão incluem:
                - Condições meteorológicas (vento, temperatura, umidade)
                - Propriedades da substância (densidade, volatilidade, toxicidade)
                - Topografia do terreno
                - Características da fonte de liberação
                """,
                """
                Modelos de Dispersão Atmosférica são ferramentas matemáticas que simulam o transporte 
                e diluição de poluentes na atmosfera. Os modelos mais comuns incluem:
                
                1. Modelo Gaussiano: Assume distribuição normal da concentração
                2. Modelo de Caixa: Considera volume fixo de mistura
                3. Modelos CFD: Dinâmica de fluidos computacional para casos complexos
                
                Cada modelo tem suas aplicações específicas dependendo da escala e complexidade do cenário.
                """,
                """
                Parâmetros Meteorológicos Críticos para dispersão:
                
                - Velocidade do vento: Determina a taxa de transporte horizontal
                - Direção do vento: Define a trajetória da pluma
                - Estabilidade atmosférica: Influencia a dispersão vertical
                - Temperatura: Afeta a densidade e reações químicas
                - Umidade relativa: Importante para substâncias higroscópicas
                - Pressão atmosférica: Influencia a densidade do ar
                
                A classificação de estabilidade de Pasquill-Gifford é amplamente utilizada.
                """,
            ]

            metadata = [
                {"source": "manual_basico", "topic": "introducao"},
                {"source": "manual_basico", "topic": "modelos"},
                {"source": "manual_basico", "topic": "meteorologia"},
            ]

            return self.process_documents(default_docs, metadata)

        except Exception as e:
            logger.error(f"Erro ao carregar documentos padrão: {e}")
            return False


# Instância global do sistema RAG
rag_system = None


def get_rag_system() -> RAGSystem:
    """Retorna instância do sistema RAG"""
    global rag_system
    if rag_system is None:
        rag_system = RAGSystem()
        # Carregar documentos padrão ao inicializar o sistema.
        # Decisão: garantir que o sistema sempre tenha conhecimento mínimo para responder perguntas.
        rag_system.load_default_documents()
    return rag_system
