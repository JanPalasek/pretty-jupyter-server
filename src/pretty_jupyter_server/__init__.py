from fastapi import Depends, FastAPI, Request, Response, UploadFile

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from pathlib import Path
import io
import shutil
import tempfile
import os
import zipfile

from traitlets.config import Config
from nbconvert.exporters import HTMLExporter

from fastapi.responses import FileResponse


app = FastAPI()

ALLOWED_ORIGINS = ["http://janpalasek.com"]

app.add_middleware(CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"])

# Salt to your taste
# ALLOWED_ORIGINS = "http://janpalasek.com"    # or 'foo.com', etc.

# handle CORS preflight requests
# @app.options('/{rest_of_path:path}')
# async def preflight_handler(request: Request, rest_of_path: str) -> Response:
#     response = Response()
#     response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS
#     response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
#     response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
#     return response

# # set CORS headers
# @app.middleware("http")
# async def add_CORS_header(request: Request, call_next):
#     response = await call_next(request)
#     response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS
#     response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
#     response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
#     return response


tempfile.tempdir = "tmp/"

if not os.path.exists(tempfile.gettempdir()):
    os.makedirs(tempfile.gettempdir())


def create_tmpdir():
    """
    Create temporary directory
    """
    tmpdir = tempfile.mkdtemp()
    try:
        yield tmpdir
    finally:
        shutil.rmtree(tmpdir)

@app.post("/nbconvert/")
async def nbconvert(file: UploadFile, tmpdir: str = Depends(create_tmpdir)):
    content = await file.read()

    config =  Config()
    config.HTMLExporter.template_name = "pj"
    exporter = HTMLExporter(config)

    with io.BytesIO(content) as buffer, io.TextIOWrapper(buffer, encoding="utf-8") as file_input:
        output = exporter.from_file(file_input)[0]

    # write to temp file
    file_stem = Path(file.filename).stem
    file_dest = os.path.join(tmpdir, f"{file_stem}.html")
    with open(file_dest, "w", encoding="utf-8") as file_w:
        file_w.write(output)

    # make archive from the temp
    zip_dest = os.path.join(os.path.abspath(tmpdir), f"{file_stem}.zip")

    # convert zipfile
    with zipfile.ZipFile(zip_dest, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(file_dest, arcname=os.path.basename(file_dest))

    return FileResponse(path=zip_dest, filename=os.path.basename(zip_dest))
