from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tempfile
import shutil
import os

app = FastAPI(
    title="Echo-See Backend API",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

classify_sound = None


@app.get("/")
def root():
    return {"message": "Echo-See Backend API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/detect_sound")
async def detect_sound(file: UploadFile = File(...)):
    global classify_sound

    if classify_sound is None:
        from models.sound_classifier import classify_sound

    if not file.filename.endswith(".wav"):
        return JSONResponse(
            status_code=400,
            content={"error": "Only .wav files supported"}
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        shutil.copyfileobj(file.file, tmp)
        audio_path = tmp.name

    try:
        label, confidence = classify_sound(audio_path)
    except Exception as e:
        os.remove(audio_path)
        return JSONResponse(status_code=500, content={"error": str(e)})

    os.remove(audio_path)

    return {"label": label, "confidence": float(confidence)}


@app.post("/direction")
async def direction():
    return JSONResponse(status_code=501, content={"message": "Not integrated"})


@app.post("/captions")
async def captions():
    return JSONResponse(status_code=501, content={"message": "Not integrated"})
