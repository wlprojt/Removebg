from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root route (for browser + health check)
@app.get("/")
def root():
    return {"message": "API is running 🚀"}

# ✅ Main API route
@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    try:
        if not file.content_type.startswith("image/"):
            return {"error": "Only image files allowed"}

        input_bytes = await file.read()
        output_bytes = remove(input_bytes)

        return Response(content=output_bytes, media_type="image/png")

    except Exception as e:
        return {"error": str(e)}