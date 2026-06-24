from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from scanner import scan_orphan_raws

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="PIXIE RAW File Manager")

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


class ScanRequest(BaseModel):
    source_path: str
    dry_run: bool = True
    delete_after_move: bool = False


@app.get("/")
async def home():
    return FileResponse(
        BASE_DIR / "templates" / "index.html"
    )


@app.post("/scan")
async def run_scan(payload: ScanRequest):

    return scan_orphan_raws(
        source_path=payload.source_path,
        dry_run=payload.dry_run,
        delete_after_move=payload.delete_after_move
    )