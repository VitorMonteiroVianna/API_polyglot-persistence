import os
import chromadb

from typing import List
from chromadb.utils import embedding_functions

from app.users.models import User
from app.genai.interfaces.i_genai_hander import IGenaiHander
from app.genai.available_models import AvailableModels
from app.chat.schemas.embedding import EmbeddingPayload, EmbeddingResponse
from app.shared import utils
from app.chat.interfaces.runners.i_embedding_runner import IEmbeddingRunner


class EmbeddingRunner(IEmbeddingRunner):
    """
    Classe responsável por gerar e armazenar embeddings no banco vetorial Chroma.
    """

    def __init__(self, user: User, genai_handler: IGenaiHander):
        self.__user = user
        self.__genai_handler = genai_handler

        self.__client = self.__start_chroma_client()
        self.__collection = self.__get_or_create_collection()

    def __start_chroma_client(self):
        """
        Inicializa o ChromaDB local com persistência em disco.
        """
        db_path = "data/chroma_db"
        os.makedirs(db_path, exist_ok=True)
        return chromadb.PersistentClient(path=db_path)

    def __get_or_create_collection(self):
        """
        Cria ou acessa a coleção vetorial padrão do usuário.
        Cada usuário tem sua própria coleção, isolada por ID.
        """
        collection_name = f"user_{self.__user.id}_embeddings"
        return self.__client.get_or_create_collection(name=collection_name)

    def enrich_prompt(self, prompt: str, model: AvailableModels = AvailableModels.OPENAI_EMBEDDING_3_SMALL, top_k: int = 3) -> str:
        """
        Retorna o prompt enriquecido com informações relevantes do banco vetorial.
        - Gera o embedding do prompt
        - Busca os embeddings mais similares
        - Retorna um prompt contextualizado
        """
        prompt_vector = self.__genai_handler.get_embedding(
            text=prompt,
            model=model
        )

        results = self.__collection.query(
            query_embeddings=[prompt_vector],
            n_results=top_k
        )

        retrieved_docs: List[str] = results.get("documents", [[]])[0]

        if not retrieved_docs:
            return prompt

        context_text = "\n".join(retrieved_docs)

        enriched_prompt = (
            f"Contexto relevante:\n{context_text}\n\n"
            f"Pergunta original:\n{prompt}"
        )

        return enriched_prompt


    def run(self, payload: EmbeddingPayload) -> EmbeddingResponse:
        """
        Gera o embedding via GenaiHandler e salva no Chroma.
        """
        embedding_vector = self.__genai_handler.get_embedding(
            text=payload.text,
            model=payload.model
        )

        embedding_id = utils.generate_hash_id()

        self.__collection.add(
            ids=[embedding_id],
            documents=[payload.text],
            embeddings=[embedding_vector],
        )

        return EmbeddingResponse(
            id=embedding_id,
            text=payload.text,
            vector=embedding_vector,
            dimension=len(embedding_vector)
        )
