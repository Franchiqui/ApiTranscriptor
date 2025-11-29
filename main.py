from fastapi import FastAPI, UploadFile, File
from io import BytesIO
import librosa
import numpy as np
from scipy.io import wavfile
import speech_recognition as sr
import uvicorn

app = FastAPI()

def transcribir_archivo_audio(contents: bytes):
    try:
        # Cargar audio con librosa
        audio_data, samplerate = librosa.load(BytesIO(contents), sr=None)
        
        # Convertir a mono si es estéreo
        if len(audio_data.shape) > 1:
            audio_data = librosa.to_mono(audio_data)
        
        # Resamplear a 16kHz si es necesario
        if samplerate != 16000:
            audio_data = librosa.resample(audio_data, orig_sr=samplerate, target_sr=16000)
            samplerate = 16000
        
        # Convertir a formato de 16-bit para WAV
        audio_int16 = (audio_data * 32767).astype(np.int16)
        
        # Crear archivo WAV en memoria
        wav_buffer = BytesIO()
        wavfile.write(wav_buffer, samplerate, audio_int16)
        wav_buffer.seek(0)
        
        # Transcribir con speech_recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_buffer) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="es-ES")
        
        return {"transcription": text}
    
    except Exception as e:
        return {"error": f"Error en transcripción: {str(e)}"}

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    contents = await file.read()
    result = transcribir_archivo_audio(contents)
    return result

@app.get("/")
async def root():
    return {"message": "API de transcripción de audio"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)