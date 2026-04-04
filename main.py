from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove, new_session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API is running 🚀"}

# 🔥 Lazy load session (IMPORTANT)
session = None

def get_session():
    global session
    if session is None:
        session = new_session("u2netp")  # ✅ lightweight model
    return session

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    try:
        if not file.content_type.startswith("image/"):
            return {"error": "Only image files allowed"}

        input_bytes = await file.read()

        # 🔥 use lazy session
        output_bytes = remove(input_bytes, session=get_session())

        return Response(content=output_bytes, media_type="image/png")

    except Exception as e:
        return {"error": str(e)}