
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove

app = FastAPI()

# ✅ MUST BE HERE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def remove_bg(file: UploadFile = File(...)):
    input_bytes = await file.read()
    output_bytes = remove(input_bytes)
    return Response(content=output_bytes, media_type="image/png")