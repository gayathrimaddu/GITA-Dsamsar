# GITA:Dsamsar — Companion of Life

Starter MVP for an AI companion using Gemini and a sacred-text knowledge base.

## Run locally (Windows)

1. Open this folder in VS Code.
2. Create a virtual environment:
   `python -m venv .venv`
3. Activate:
   `.venv\Scripts\activate`
4. Install:
   `pip install -r requirements.txt`
5. Copy `.env.example` to `.env`.
6. Put your Gemini API key in `.env`:
   `GEMINI_API_KEY=your_key`
7. Start:
   `uvicorn main:app --reload`
8. Open:
   `http://127.0.0.1:8000/app/`

Next upgrades:
- Replace starter knowledge with a properly sourced Bhagavad Gita + Upanishad corpus.
- Add embeddings/vector retrieval.
- Show precise source/chapter/verse metadata.
- Add conversation memory.
- Deploy to Google Cloud Run.
