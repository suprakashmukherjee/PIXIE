from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel

from scanner import scan_orphan_raws

app = FastAPI(title="PIXIE RAW File Manager")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


class ScanRequest(BaseModel):
    source_path: str
    delete_folder: str
    dry_run: bool = True
    delete_after_move: bool = False


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={}
)


@app.post("/scan")
async def run_scan(payload: ScanRequest):

    result = scan_orphan_raws(
        source_path=payload.source_path,
        delete_folder=payload.delete_folder,
        delete_after_move=payload.delete_after_move,
        dry_run=payload.dry_run
    )

    return result