import os

os.environ["HOME"] = "/tmp"
os.environ["U2NET_HOME"] = "/tmp"
os.environ["XDG_CACHE_HOME"] = "/tmp"
os.environ["NUMBA_CACHE_DIR"] = "/tmp"

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove, new_session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

session = None

def get_session():
    global session
    if session is None:
        session = new_session("u2netp")
    return session

@app.get("/")
def root():
    return {"message": "API is running 🚀"}

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    try:
        input_bytes = await file.read()
        output_bytes = remove(input_bytes, session=get_session())
        return Response(content=output_bytes, media_type="image/png")
    except Exception as e:
        return {"error": str(e)}