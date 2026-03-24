import os

from openai import OpenAI


LLM_BASE_URL = os.getenv("LLM_BASE_URL", "").strip()
LLM_API_KEY = os.getenv("LLM_API_KEY", "ollama")
LLM_MODEL = os.getenv("LLM_MODEL", "").strip()
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.2"))


class LLMNotConfiguredError(RuntimeError):
    pass


def llm_is_configured() -> bool:
    return bool(LLM_BASE_URL and LLM_MODEL)


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
        "Wenn Informationen fehlen oder nur teilweise vorhanden sind, benenne das klar. "
        "Halte dich exakt an dieses Antwortschema:\n"
        "1. Kurzantwort\n"
        "2. Wichtige Punkte\n"
        "3. Unsicherheiten oder Luecken\n"
        "4. Quellen"
    )
    user_prompt = (
        f"Space: {space_name}\n\n"
        f"Kontext:\n{context_text}\n\n"
        f"Frage:\n{question}\n\n"
        "Regeln:\n"
        "- Unter 'Kurzantwort' 2 bis 4 Saetze.\n"
        "- Unter 'Wichtige Punkte' 3 bis 6 Aufzaehlungspunkte.\n"
        "- Unter 'Unsicherheiten oder Luecken' nur Punkte nennen, die wirklich offen sind.\n"
        "- Unter 'Quellen' nur die im Kontext vorhandenen Quellen nennen.\n"
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
    return message.strip()
