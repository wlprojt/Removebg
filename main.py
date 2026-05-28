import os

os.environ["U2NET_HOME"] = "/tmp"
os.environ["XDG_CACHE_HOME"] = "/tmp"


from fastapi import FastAPI, UploadFile, File, HTTPException
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
async def root():
    return {"message": "RemoveBG API Running 🚀"}

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Only image files allowed")

        input_bytes = await file.read()

        output_bytes = remove(
            input_bytes,
            session=get_session()
        )

        return Response(
            content=output_bytes,
            media_type="image/png"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))