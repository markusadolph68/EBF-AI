import os
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from mlx_lm import generate, load


MODEL_NAME = os.getenv("MLX_MODEL_NAME", "NexVeridian/Qwen3.5-4B-5bit")
HOST = os.getenv("MLX_HOST", "0.0.0.0")
PORT = int(os.getenv("MLX_PORT", "8000"))

app = FastAPI(title="EBF MLX OpenAI Server")
model, tokenizer = load(MODEL_NAME)


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatCompletionRequest(BaseModel):
    model: str | None = None
    messages: list[Message]
    max_tokens: int = 500
    temperature: float = 0.2


class CompletionRequest(BaseModel):
    model: str | None = None
    prompt: str
    max_tokens: int = 500
    temperature: float = 0.2


def build_prompt(messages: list[Message]) -> str:
    if tokenizer.chat_template is not None:
        chat_messages = [{"role": item.role, "content": item.content} for item in messages]
        return tokenizer.apply_chat_template(
            chat_messages,
            tokenize=False,
            add_generation_prompt=True,
        )

    lines = []
    for item in messages:
        lines.append(f"{item.role.title()}: {item.content.strip()}")
    lines.append("Assistant:")
    return "\n".join(lines)


def generate_text(prompt: str, max_tokens: int) -> str:
    return generate(
        model,
        tokenizer,
        prompt=prompt,
        max_tokens=max_tokens,
        verbose=False,
    )


@app.get("/")
def root():
    return {
        "service": "ebf-mlx-openai-server",
        "status": "ok",
        "model": MODEL_NAME,
    }


@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL_NAME}


@app.get("/v1/models")
def list_models():
    return {
        "object": "list",
        "data": [
            {
                "id": MODEL_NAME,
                "object": "model",
                "owned_by": "local-mlx",
            }
        ],
    }


@app.post("/v1/completions")
def completions(req: CompletionRequest):
    try:
        text = generate_text(req.prompt, req.max_tokens)
        return {
            "id": "cmpl-ebf-mlx",
            "object": "text_completion",
            "model": MODEL_NAME,
            "choices": [
                {
                    "index": 0,
                    "text": text,
                    "finish_reason": "stop",
                }
            ],
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/v1/chat/completions")
def chat_completions(req: ChatCompletionRequest):
    try:
        prompt = build_prompt(req.messages)
        text = generate_text(prompt, req.max_tokens)
        return {
            "id": "chatcmpl-ebf-mlx",
            "object": "chat.completion",
            "model": MODEL_NAME,
            "choices": [
                {
                    "index": 0,
                    "finish_reason": "stop",
                    "message": {
                        "role": "assistant",
                        "content": text,
                    },
                }
            ],
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
