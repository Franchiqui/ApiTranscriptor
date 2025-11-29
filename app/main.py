from fastapi import FastAPI, UploadFile, File
from .transcriptor import transcribir_archivo_audio

app = FastAPI()

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    contents = await file.read()
    result = transcribir_archivo_audio(contents)
    return result

@app.get("/")
async def root():
    return {"message": "API de transcripción de audio"}
