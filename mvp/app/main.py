import os
import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import Depends, FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from database import Base, engine, get_db
from docling_ingest import ensure_dir, sha256_file
from llm import LLMNotConfiguredError, answer_question, llm_is_configured
from models import Document, Space, User
from rag import ingest_document, query_space
from security import hash_password, verify_password


APP_NAME = os.getenv("APP_NAME", "EBF AI MVP")
APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "change-me")
DEFAULT_CHUNK_SIZE = int(os.getenv("DEFAULT_CHUNK_SIZE", "350"))
DEFAULT_CHUNK_OVERLAP = int(os.getenv("DEFAULT_CHUNK_OVERLAP", "50"))
DEFAULT_RETRIEVAL_K = int(os.getenv("DEFAULT_RETRIEVAL_K", "4"))

DATA_DIR = Path("/data")
UPLOAD_DIR = DATA_DIR / "uploads"
PROCESSED_DIR = DATA_DIR / "processed"

ensure_dir(UPLOAD_DIR)
ensure_dir(PROCESSED_DIR)

Base.metadata.create_all(bind=engine)

app = FastAPI(title=APP_NAME)
app.add_middleware(SessionMiddleware, secret_key=APP_SECRET_KEY, same_site="lax")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def set_flash(request: Request, message: str, level: str = "info") -> None:
    request.session["flash"] = {"message": message, "level": level}


def pop_flash(request: Request):
    return request.session.pop("flash", None)


def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return db.get(User, user_id)


def require_user(user: User | None = Depends(get_current_user)) -> User:
    if not user:
        raise HTTPException(status_code=401)
    return user


def render(request: Request, template_name: str, context: dict):
    context.update(
        {
            "request": request,
            "app_name": APP_NAME,
            "current_user": context.get("current_user"),
            "flash": pop_flash(request),
        }
    )
    return templates.TemplateResponse(template_name, context)


@app.get("/health")
def health():
    return {"status": "ok", "app": APP_NAME}


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db), user: User | None = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    spaces = db.query(Space).filter(Space.owner_id == user.id).order_by(Space.created_at.desc()).all()
    return render(
        request,
        "dashboard.html",
        {
            "current_user": user,
            "spaces": spaces,
            "llm_ready": llm_is_configured(),
            "default_chunk_size": DEFAULT_CHUNK_SIZE,
            "default_chunk_overlap": DEFAULT_CHUNK_OVERLAP,
        },
    )


@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request, user: User | None = Depends(get_current_user)):
    if user:
        return RedirectResponse(url="/", status_code=303)
    return render(request, "register.html", {})


@app.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    username = username.strip().lower()
    if len(username) < 3 or len(password) < 8:
        set_flash(request, "Benutzername oder Passwort ist zu kurz.", "error")
        return RedirectResponse(url="/register", status_code=303)

    existing = db.query(User).filter(User.username == username).first()
    if existing:
        set_flash(request, "Benutzername existiert bereits.", "error")
        return RedirectResponse(url="/register", status_code=303)

    user = User(username=username, password_hash=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    request.session["user_id"] = user.id
    set_flash(request, "Benutzer wurde angelegt.", "success")
    return RedirectResponse(url="/", status_code=303)


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request, user: User | None = Depends(get_current_user)):
    if user:
        return RedirectResponse(url="/", status_code=303)
    return render(request, "login.html", {})


@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    username = username.strip().lower()
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        set_flash(request, "Login fehlgeschlagen.", "error")
        return RedirectResponse(url="/login", status_code=303)

    request.session["user_id"] = user.id
    set_flash(request, "Login erfolgreich.", "success")
    return RedirectResponse(url="/", status_code=303)


@app.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)


@app.get("/spaces/new", response_class=HTMLResponse)
def new_space_page(request: Request, user: User = Depends(require_user)):
    return render(
        request,
        "space_new.html",
        {
            "current_user": user,
            "default_chunk_size": DEFAULT_CHUNK_SIZE,
            "default_chunk_overlap": DEFAULT_CHUNK_OVERLAP,
            "default_retrieval_k": DEFAULT_RETRIEVAL_K,
        },
    )


@app.post("/spaces/new")
async def create_space(
    request: Request,
    name: str = Form(...),
    description: str = Form(""),
    chunk_size: int = Form(DEFAULT_CHUNK_SIZE),
    chunk_overlap: int = Form(DEFAULT_CHUNK_OVERLAP),
    retrieval_k: int = Form(DEFAULT_RETRIEVAL_K),
    user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    name = name.strip()
    if not name:
        set_flash(request, "Space-Name fehlt.", "error")
        return RedirectResponse(url="/spaces/new", status_code=303)

    space = Space(
        owner_id=user.id,
        name=name,
        description=description.strip(),
        chunk_size=max(50, chunk_size),
        chunk_overlap=max(0, min(chunk_overlap, chunk_size - 1)),
        retrieval_k=max(1, min(retrieval_k, 10)),
    )
    db.add(space)
    db.commit()
    db.refresh(space)
    ensure_dir(UPLOAD_DIR / str(space.id))
    set_flash(request, "Space wurde angelegt.", "success")
    return RedirectResponse(url=f"/spaces/{space.id}", status_code=303)


def get_owned_space(space_id: int, user_id: int, db: Session) -> Space:
    space = db.query(Space).filter(Space.id == space_id, Space.owner_id == user_id).first()
    if not space:
        raise HTTPException(status_code=404, detail="Space nicht gefunden")
    return space


@app.get("/spaces/{space_id}", response_class=HTMLResponse)
def space_detail(
    space_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
):
    space = get_owned_space(space_id, user.id, db)
    documents = db.query(Document).filter(Document.space_id == space.id).order_by(Document.created_at.desc()).all()
    return render(
        request,
        "space_detail.html",
        {
            "current_user": user,
            "space": space,
            "documents": documents,
            "answer": None,
            "sources": [],
            "retrieval_contexts": [],
            "question": "",
            "llm_ready": llm_is_configured(),
        },
    )


@app.post("/spaces/{space_id}/upload")
async def upload_documents(
    space_id: int,
    request: Request,
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
):
    space = get_owned_space(space_id, user.id, db)
    target_dir = UPLOAD_DIR / str(space.id)
    ensure_dir(target_dir)

    uploaded_count = 0
    for upload in files:
        if not upload.filename:
            continue

        destination = target_dir / f"{uuid4().hex}_{upload.filename}"
        with destination.open("wb") as handle:
            shutil.copyfileobj(upload.file, handle)

        checksum = sha256_file(destination)
        document = Document(
            space_id=space.id,
            original_name=upload.filename,
            stored_path=str(destination),
            checksum=checksum,
            status="processing",
        )
        db.add(document)
        db.commit()
        db.refresh(document)

        try:
            chunk_count = ingest_document(space, document, destination)
            document.status = "ready"
            document.chunk_count = chunk_count
            document.error_message = ""
            uploaded_count += 1
        except Exception as exc:
            document.status = "error"
            document.error_message = str(exc)
            document.chunk_count = 0
        finally:
            db.add(document)
            db.commit()

    if uploaded_count:
        set_flash(request, f"{uploaded_count} Dokument(e) verarbeitet.", "success")
    else:
        set_flash(request, "Kein Dokument erfolgreich verarbeitet.", "error")

    return RedirectResponse(url=f"/spaces/{space.id}", status_code=303)


@app.post("/spaces/{space_id}/chat", response_class=HTMLResponse)
async def chat_with_space(
    space_id: int,
    request: Request,
    question: str = Form(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_user),
):
    space = get_owned_space(space_id, user.id, db)
    documents = db.query(Document).filter(Document.space_id == space.id).order_by(Document.created_at.desc()).all()

    answer = None
    sources: list[str] = []
    retrieval_contexts = []
    try:
        context_blocks, sources = query_space(space, question)
        retrieval_contexts = context_blocks
        if not context_blocks:
            set_flash(request, "Im Space wurden noch keine passenden Wissensdaten gefunden.", "info")
        else:
            answer = answer_question(space.name, question, context_blocks)
    except LLMNotConfiguredError as exc:
        set_flash(request, str(exc), "error")
    except Exception as exc:
        set_flash(request, f"Chat fehlgeschlagen: {exc}", "error")

    return render(
        request,
        "space_detail.html",
        {
            "current_user": user,
            "space": space,
            "documents": documents,
            "answer": answer,
            "sources": sources,
            "retrieval_contexts": retrieval_contexts,
            "question": question,
            "llm_ready": llm_is_configured(),
        },
    )
