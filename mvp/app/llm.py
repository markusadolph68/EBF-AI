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
    context_text = "\n\n---\n\n".join(context_blocks) if context_blocks else "Keine Quellen gefunden."

    system_prompt = (
        "Du bist ein interner Wissensassistent. "
        "Antworte auf Deutsch, knapp und praezise. "
        "Nutze nur den bereitgestellten Kontext. "
        "Wenn der Kontext nicht ausreicht, sage klar, dass die Information im Space nicht gefunden wurde."
    )
    user_prompt = (
        f"Space: {space_name}\n\n"
        f"Kontext:\n{context_text}\n\n"
        f"Frage:\n{question}\n\n"
        "Erzeuge eine hilfreiche Antwort und nenne am Ende kurz die verwendeten Quellen."
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

