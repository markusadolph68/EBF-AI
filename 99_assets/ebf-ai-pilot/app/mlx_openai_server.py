import os
from typing import List, Optional, Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mlx_lm import load, generate

MODEL_NAME = os.getenv("MODEL_NAME", "mlx-community/Llama-3.2-3B-Instruct")

app = FastAPI(title="MLX OpenAI-Compatible Server")

model, tokenizer = load(MODEL_NAME)

class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

class ChatCompletionRequest(BaseModel):
    model: Optional[str] = None
    messages: List[Message]
    max_tokens: int = 300
    temperature: float = 0.2

class CompletionRequest(BaseModel):
    model: Optional[str] = None
    prompt: str
    max_tokens: int = 300
    temperature: float = 0.2

def build_prompt(messages: List[Message]) -> str:
    system_parts = []
    conversation_parts = []

    for msg in messages:
        if msg.role == "system":
            system_parts.append(msg.content.strip())
        elif msg.role == "user":
            conversation_parts.append(f"User: {msg.content.strip()}")
        elif msg.role == "assistant":
            conversation_parts.append(f"Assistant: {msg.content.strip()}")

    system_text = "\n".join(system_parts).strip()
    convo_text = "\n".join(conversation_parts).strip()

    if system_text:
        return f"{system_text}\n\n{convo_text}\nAssistant:"
    return f"{convo_text}\nAssistant:"

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
                "owned_by": "local-mlx"
            }
        ]
    }

@app.post("/v1/completions")
def completions(req: CompletionRequest):
    try:
        text = generate(
            model,
            tokenizer,
            prompt=req.prompt,
            max_tokens=req.max_tokens,
        )
        return {
            "id": "cmpl-local-mlx",
            "object": "text_completion",
            "model": MODEL_NAME,
            "choices": [
                {
                    "index": 0,
                    "text": text,
                    "finish_reason": "stop"
                }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/chat/completions")
def chat_completions(req: ChatCompletionRequest):
    try:
        prompt = build_prompt(req.messages)
        text = generate(
            model,
            tokenizer,
            prompt=prompt,
            max_tokens=req.max_tokens,
        )
        return {
            "id": "chatcmpl-local-mlx",
            "object": "chat.completion",
            "model": MODEL_NAME,
            "choices": [
                {
                    "index": 0,
                    "finish_reason": "stop",
                    "message": {
                        "role": "assistant",
                        "content": text
                    }
                }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
