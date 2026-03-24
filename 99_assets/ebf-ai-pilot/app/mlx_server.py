from fastapi import FastAPI
from pydantic import BaseModel
from mlx_lm import load, generate

app = FastAPI()

MODEL_NAME = "mlx-community/Llama-3.2-3B-Instruct"
model, tokenizer = load(MODEL_NAME)

class CompletionRequest(BaseModel):
    prompt: str
    max_tokens: int = 300

@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL_NAME}

@app.post("/v1/completions")
def completions(req: CompletionRequest):
    text = generate(
        model,
        tokenizer,
        prompt=req.prompt,
        max_tokens=req.max_tokens
    )
    return {
        "id": "mlx-local",
        "object": "text_completion",
        "choices": [
            {
                "index": 0,
                "text": text,
                "finish_reason": "stop"
            }
        ]
    }
