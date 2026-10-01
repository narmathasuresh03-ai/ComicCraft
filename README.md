# ComicCraft - Corrected Project

This version fixes the frontend/backend endpoint mismatch.

## Setup

1. Open this ROOT folder in VS Code.
2. Run:
   `py --version`
3. Create environment:
   `py -3.12 -m venv .venv`
4. Activate:
   `.venv\Scripts\Activate.ps1`
5. Install:
   `python -m pip install --upgrade pip`
   `python -m pip install -r requirements.txt`
6. Copy `.env.example` to `.env`.
7. Put your real key in `.env`:
   `GEMINI_API_KEY=YOUR_REAL_KEY_HERE`
   `GEMINI_MODEL=gemini-2.5-flash`
8. Run from the ROOT folder:
   `python run.py`
9. Open:
   `http://127.0.0.1:8000`

The frontend calls `/api/generate`, matching the FastAPI route in `app/routes.py`.
Do not share your real API key or commit `.env` to GitHub.
