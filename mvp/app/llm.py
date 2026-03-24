import os
import re

from openai import OpenAI


LLM_BASE_URL = os.getenv("LLM_BASE_URL", "").strip()
LLM_API_KEY = os.getenv("LLM_API_KEY", "ollama")
LLM_MODEL = os.getenv("LLM_MODEL", "").strip()
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.2"))


class LLMNotConfiguredError(RuntimeError):
    pass


def llm_is_configured() -> bool:
    return bool(LLM_BASE_URL and LLM_MODEL)


def sanitize_answer(text: str) -> str:
    cleaned = text.strip()

    # Remove common reasoning preambles some small models emit.
    patterns = [
        r"(?is)^thinking process:\s*",
        r"(?is)^analysis:\s*",
        r"(?is)^reasoning:\s*",
    ]
    for pattern in patterns:
        cleaned = re.sub(pattern, "", cleaned).strip()

    # If the model emitted chain-of-thought before the requested structure,
    # keep only the structured part starting at "Kurzantwort".
    match = re.search(r"(?is)(kurzantwort.*)", cleaned)
    if match:
        cleaned = match.group(1).strip()

    return cleaned


def answer_question(space_name: str, question: str, context_blocks: list[str]) -> str:
    if not llm_is_configured():
        raise LLMNotConfiguredError(
            "LLM_BASE_URL und LLM_MODEL muessen gesetzt sein, damit Chat funktioniert."
        )

    client = OpenAI(base_url=LLM_BASE_URL, api_key=LLM_API_KEY)
    context_text = (
        "\n\n---\n\n".join(
            [
                (
                    f"Quelle: {item['source_file']} | Chunk: {item['chunk_index']}\n"
                    f"{item['text']}"
                )
                for item in context_blocks
            ]
        )
        if context_blocks
        else "Keine Quellen gefunden."
    )

    system_prompt = (
        "Du bist ein interner Wissensassistent. "
        "Antworte auf Deutsch. "
        "Nutze ausschliesslich den bereitgestellten Kontext. "
        "Erfinde nichts. "
        "Gib niemals deinen Denkprozess, keine Analyse und keine internen Zwischenschritte aus. "
        "Wenn Informationen fehlen oder nur teilweise vorhanden sind, benenne das klar. "
        "Halte dich exakt an dieses Antwortschema:\n"
        "Kurzantwort:\n"
        "Wichtige Punkte:\n"
        "Unsicherheiten oder Luecken:\n"
        "Quellen:"
    )
    user_prompt = (
        f"Space: {space_name}\n\n"
        f"Kontext:\n{context_text}\n\n"
        f"Frage:\n{question}\n\n"
        "Regeln:\n"
        "- Unter 'Kurzantwort' 2 bis 4 Saetze.\n"
        "- Unter 'Wichtige Punkte' 3 bis 6 kurze Aufzaehlungspunkte.\n"
        "- Unter 'Unsicherheiten oder Luecken' nur Punkte nennen, die wirklich offen sind.\n"
        "- Unter 'Quellen' nur die im Kontext vorhandenen Quellen nennen.\n"
        "- Keine englischen Ueberschriften verwenden.\n"
        "- Keine Begriffe wie 'Thinking Process', 'Analysis', 'Reasoning' oder aehnliches ausgeben.\n"
        "- Wenn der Kontext nicht reicht, sage das klar und antworte nicht spekulativ."
    )

    response = client.chat.completions.create(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    message = response.choices[0].message.content or ""
    return sanitize_answer(message)
