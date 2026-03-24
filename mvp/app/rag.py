import os
import re
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from docling_ingest import chunk_text, extract_text_with_docling, normalize_text


CHROMA_HOST = os.getenv("CHROMA_HOST", "chroma")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))
CHROMA_COLLECTION_PREFIX = os.getenv("CHROMA_COLLECTION_PREFIX", "ebf_space")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "intfloat/multilingual-e5-small")


embedding_function = SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
_client = None


def get_client():
    global _client
    if _client is None:
        _client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    return _client


def _slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "space"


def collection_name_for_space(space_id: int, space_name: str) -> str:
    return f"{CHROMA_COLLECTION_PREFIX}_{space_id}_{_slugify(space_name)}"[:63]


def get_collection(space_id: int, space_name: str):
    name = collection_name_for_space(space_id, space_name)
    return get_client().get_or_create_collection(name=name, embedding_function=embedding_function)


def ingest_document(space, document, file_path: Path) -> int:
    collection = get_collection(space.id, space.name)
    raw_text = extract_text_with_docling(file_path)
    normalized_text = normalize_text(raw_text)
    chunks = chunk_text(normalized_text, space.chunk_size, space.chunk_overlap)

    if not chunks:
        raise RuntimeError(f"No chunks produced for {file_path.name}")

    ids = [f"doc-{document.id}-chunk-{idx}" for idx, _ in enumerate(chunks)]
    metadatas = []
    for idx, _ in enumerate(chunks):
        metadatas.append(
            {
                "space_id": space.id,
                "document_id": document.id,
                "source_file": document.original_name,
                "chunk_index": idx,
            }
        )

    collection.add(ids=ids, documents=chunks, metadatas=metadatas)
    return len(chunks)


def query_space(space, question: str):
    collection = get_collection(space.id, space.name)
    if collection.count() == 0:
        return [], []

    result = collection.query(query_texts=[question], n_results=space.retrieval_k)

    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]

    context_blocks = []
    sources = []
    seen_keys = set()
    for idx, document_text in enumerate(documents):
        metadata = metadatas[idx] if idx < len(metadatas) else {}
        source_file = metadata.get("source_file", "unbekannt")
        chunk_index = metadata.get("chunk_index", "?")
        source_key = f"{source_file}:{chunk_index}"
        clean_text = " ".join(str(document_text).split())
        preview = clean_text[:600].strip()

        if source_key in seen_keys:
            continue
        seen_keys.add(source_key)

        context_blocks.append(
            {
                "source_file": source_file,
                "chunk_index": chunk_index,
                "text": preview,
            }
        )
        sources.append(
            {
                "source_file": source_file,
                "chunk_index": chunk_index,
                "label": f"{source_file} (Chunk {chunk_index})",
            }
        )

    return context_blocks, sources
