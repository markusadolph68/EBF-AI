import hashlib
import os
import re
from pathlib import Path


def sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            hasher.update(chunk)
    return f"sha256:{hasher.hexdigest()}"


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
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")

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
            if overlap:
                current_words = current_words[-overlap:]
            else:
                current_words = []

        while len(words) > chunk_size:
            window = words[:chunk_size]
            chunks.append(" ".join(window).strip())
            if overlap:
                words = words[chunk_size - overlap :]
            else:
                words = words[chunk_size:]

        current_words.extend(words)

    if current_words:
        chunks.append(" ".join(current_words).strip())

    return [chunk for chunk in chunks if chunk]


def ensure_dir(path: Path) -> None:
    os.makedirs(path, exist_ok=True)

