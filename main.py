from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

from config import settings
from routes import router

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title=settings.app_name)

templates = Jinja2Templates(directory=str(BASE_DIR))

app.include_router(router)


@app.get("/static/style.css")
async def style_css():
    return FileResponse(
        BASE_DIR / "style.css",
        media_type="text/css"
    )


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": settings.app_name}
    )
