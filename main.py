import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = FastAPI(title="GITA:Dsamsar")
BASE_DIR = Path(__file__).resolve().parent

# Load a small starter knowledge base.
# We will replace/expand this with a proper Gita + Upanishad corpus in the next step.
KB = []
kb_path = BASE_DIR / "data" / "knowledge.txt"
if kb_path.exists():
    KB = [x.strip() for x in kb_path.read_text(encoding="utf-8").split("\n---\n") if x.strip()]

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

class ChatRequest(BaseModel):
    message: str

def retrieve(query: str, top_k: int = 3):
    """Simple starter retrieval. We'll upgrade this to embeddings/vector search."""
    words = {w.lower().strip(".,?!:;()[]{}") for w in query.split() if len(w) > 2}
    scored = []
    for passage in KB:
        pwords = set(passage.lower().split())
        score = len(words & pwords)
        scored.append((score, passage))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [p for score, p in scored[:top_k] if score > 0] or KB[:top_k]

@app.get("/")
def home():
    return {"status": "ok", "app": "GITA:Dsamsar", "message": "Companion of Life"}

@app.post("/chat")
def chat(req: ChatRequest):
    if not req.message.strip():
        return {"response": "Please share what is on your mind.", "sources": []}

    context = retrieve(req.message)

    prompt = f"""
You are GITA:Dsamsar — a thoughtful AI companion inspired by the Bhagavad Gita
and Upanishadic wisdom.

Your job is NOT to pretend to be a spiritual authority. Give grounded, compassionate
guidance while clearly distinguishing ancient teaching from your practical interpretation.

USER'S QUESTION:
{req.message}

RELEVANT KNOWLEDGE:
{chr(10).join(context)}

RESPONSE RULES:
1. Answer the user's actual situation first.
2. Explain the relevant teaching in simple modern language.
3. Do not invent verses, quotations, chapter numbers, or Sanskrit text.
4. If the supplied knowledge is insufficient, say so instead of fabricating a citation.
5. End with one small practical reflection/action the user can take.
6. Keep the response warm and concise.

Return:
Guidance:
<answer>

Reflection:
<one practical reflection>
"""
    chat = client.chats.create(model="gemini-3.6-flash")
    result = chat.send_message(prompt)

    return {"response": result.text, "sources": context}

app.mount("/app", StaticFiles(directory=BASE_DIR / "static", html=True), name="app")
       
