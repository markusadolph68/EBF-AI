import argparse
import hashlib
import json
import os
import re
from datetime import UTC, datetime
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction


ROOT_DIR = Path(__file__).resolve().parents[1]
DOCUMENTS_DIR = ROOT_DIR / "documents"
PROCESSED_DIR = ROOT_DIR / "processed"
MANIFEST_DIR = PROCESSED_DIR / "manifests"
SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".md", ".txt"}

CHROMA_HOST = os.getenv("CHROMA_HOST", "127.0.0.1")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8001"))
CHROMA_COLLECTION_PREFIX = os.getenv("CHROMA_COLLECTION_PREFIX", "ebf_docs")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "intfloat/multilingual-e5-small")
DEFAULT_CHUNK_SIZE = int(os.getenv("DEFAULT_CHUNK_SIZE", "350"))
DEFAULT_CHUNK_OVERLAP = int(os.getenv("DEFAULT_CHUNK_OVERLAP", "50"))

embedding_function = SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            hasher.update(chunk)
    return f"sha256:{hasher.hexdigest()}"


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_") or "document"


def load_sidecar_metadata(path: Path) -> dict:
    sidecar_path = Path(f"{path}.metadata.json")
    if not sidecar_path.exists():
        return {}
    return json.loads(sidecar_path.read_text(encoding="utf-8"))


def load_manifest(document_id: str) -> dict | None:
    manifest_path = MANIFEST_DIR / f"{document_id}.json"
    if not manifest_path.exists():
        return None
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def save_manifest(document_id: str, payload: dict) -> None:
    ensure_dir(MANIFEST_DIR)
    manifest_path = MANIFEST_DIR / f"{document_id}.json"
    manifest_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def extract_text_with_docling(path: Path) -> str:
    try:
        from docling.document_converter import DocumentConverter

        converter = DocumentConverter()
        result = converter.convert(str(path))
        document = result.document

        if hasattr(document, "export_to_markdown"):
            return document.export_to_markdown()
        if hasattr(document, "export_to_text"):
            return document.export_to_text()
    except Exception as first_error:
        try:
            from docling import Document

            document = Document.from_file(str(path))
            data = document.to_dict()
            sections = data.get("sections", [])
            text_parts = []
            for section in sections:
                text = str(section.get("text", "")).strip()
                if text:
                    text_parts.append(text)
            if text_parts:
                return "\n\n".join(text_parts)
        except Exception as second_error:
            raise RuntimeError(
                f"Docling parsing failed for {path.name}: {first_error}; fallback failed: {second_error}"
            ) from second_error

    raise RuntimeError(f"Docling produced no text for {path.name}")


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    paragraphs = [block.strip() for block in text.split("\n\n") if block.strip()]
    chunks: list[str] = []
    current_words: list[str] = []

    for paragraph in paragraphs:
        words = paragraph.split()
        if not words:
            continue

        if len(current_words) + len(words) <= chunk_size:
            current_words.extend(words)
            continue

        if current_words:
            chunks.append(" ".join(current_words).strip())
            current_words = current_words[-overlap:] if overlap else []

        while len(words) > chunk_size:
            window = words[:chunk_size]
            chunks.append(" ".join(window).strip())
            words = words[chunk_size - overlap :] if overlap else words[chunk_size:]

        current_words.extend(words)

    if current_words:
        chunks.append(" ".join(current_words).strip())

    return [chunk for chunk in chunks if chunk]


def collection_name(area: str) -> str:
    return f"{CHROMA_COLLECTION_PREFIX}_{slugify(area)}"[:63]


def infer_section(chunk_text_value: str, chunk_index: int) -> str:
    for line in chunk_text_value.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()[:120] or f"section_{chunk_index:03d}"
    return f"section_{chunk_index:03d}"


def get_collection(area: str):
    client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    return client.get_or_create_collection(
        name=collection_name(area),
        embedding_function=embedding_function,
    )


def iter_documents(selected_area: str | None) -> list[Path]:
    if not DOCUMENTS_DIR.exists():
        return []

    candidates: list[Path] = []
    for path in DOCUMENTS_DIR.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        relative = path.relative_to(DOCUMENTS_DIR)
        area = relative.parts[0] if relative.parts else "allgemein"
        if selected_area and area != selected_area:
            continue
        candidates.append(path)

    return sorted(candidates)


def upsert_document(path: Path, force: bool) -> tuple[str, str]:
    relative = path.relative_to(DOCUMENTS_DIR)
    area = relative.parts[0] if relative.parts else "allgemein"
    sidecar = load_sidecar_metadata(path)
    checksum = sha256_file(path)
    document_id = sidecar.get("document_id") or slugify(relative.with_suffix("").as_posix())
    manifest = load_manifest(document_id)

    if manifest and manifest.get("checksum") == checksum and not force:
        return "skipped", f"{relative} unveraendert"

    raw_text = extract_text_with_docling(path)
    normalized_text = normalize_text(raw_text)
    chunks = chunk_text(normalized_text, DEFAULT_CHUNK_SIZE, DEFAULT_CHUNK_OVERLAP)
    if not chunks:
        raise RuntimeError(f"No chunks produced for {relative}")

    collection = get_collection(area)
    existing = collection.get(where={"document_id": document_id})
    existing_ids = existing.get("ids", [])
    if existing_ids:
        collection.delete(ids=existing_ids)

    title = sidecar.get("title") or path.stem.replace("_", " ").replace("-", " ").strip()
    version = sidecar.get("version") or "draft"
    confidentiality = sidecar.get("confidentiality") or "internal"
    document_type = sidecar.get("document_type") or "general"
    owner = sidecar.get("owner") or area
    kb_name = sidecar.get("kb_name") or f"kb-{area}"
    tags = sidecar.get("tags") or []
    last_updated = sidecar.get("last_updated") or datetime.fromtimestamp(path.stat().st_mtime, UTC).date().isoformat()
    ingested_at = datetime.now(UTC).isoformat()

    ids = []
    documents = []
    metadatas = []

    for idx, chunk in enumerate(chunks):
        chunk_index = idx + 1
        ids.append(f"{document_id}_{chunk_index:04d}")
        documents.append(chunk)
        metadatas.append(
            {
                "chunk_id": f"{document_id}_{chunk_index:04d}",
                "document_id": document_id,
                "source_file": path.name,
                "source_path": str(relative),
                "area": area,
                "title": title,
                "version": version,
                "confidentiality": confidentiality,
                "document_type": document_type,
                "owner": owner,
                "kb_name": kb_name,
                "language": sidecar.get("language", "de"),
                "section": infer_section(chunk, chunk_index),
                "chunk_index": chunk_index,
                "checksum": checksum,
                "last_updated": last_updated,
                "ingested_at": ingested_at,
                "tags": ",".join(tags),
            }
        )

    collection.add(ids=ids, documents=documents, metadatas=metadatas)

    save_manifest(
        document_id,
        {
            "document_id": document_id,
            "source_file": path.name,
            "source_path": str(relative),
            "area": area,
            "checksum": checksum,
            "version": version,
            "confidentiality": confidentiality,
            "chunk_count": len(chunks),
            "ingested_at": ingested_at,
            "last_updated": last_updated,
        },
    )

    return "ingested", f"{relative} -> {len(chunks)} Chunks"


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest pilot documents into Chroma.")
    parser.add_argument("--area", help="Nur einen Bereich ingestieren, z. B. hr oder vertrieb.")
    parser.add_argument("--force", action="store_true", help="Dokumente auch ohne Checksum-Aenderung neu schreiben.")
    args = parser.parse_args()

    ensure_dir(PROCESSED_DIR)
    ensure_dir(MANIFEST_DIR)

    documents = iter_documents(args.area)
    if not documents:
        print("Keine Dokumente gefunden.")
        return 0

    ingested = 0
    skipped = 0

    for path in documents:
        try:
            status, message = upsert_document(path, args.force)
            print(f"[{status}] {message}")
            if status == "ingested":
                ingested += 1
            else:
                skipped += 1
        except Exception as exc:
            print(f"[error] {path.relative_to(DOCUMENTS_DIR)}: {exc}")

    print(f"Fertig. ingestiert={ingested}, uebersprungen={skipped}, gesamt={len(documents)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
