from pydub import AudioSegment
import io
import speech_recognition as sr

def transcribir_archivo_audio(contents: bytes):
    try:
        # Cargar audio con pydub
        audio = AudioSegment.from_file(io.BytesIO(contents))
        
        # Convertir a mono si es estéreo
        if audio.channels > 1:
            audio = audio.set_channels(1)
        
        # Resamplear a 16kHz si es necesario
        if audio.frame_rate != 16000:
            audio = audio.set_frame_rate(16000)
        
        # Exportar a WAV en memoria
        wav_buffer = io.BytesIO()
        audio.export(wav_buffer, format="wav")
        wav_buffer.seek(0)
        
        # Transcribir con speech_recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_buffer) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="es-ES")
        
        return {"transcription": text}
    
    except Exception as e:
        error_str = str(e)
        if "ffprobe" in error_str or "ffmpeg" in error_str:
            return {"error": "Archivo no soportado. Convierte el audio a formato WAV antes de subir."}
        else:
            return {"error": f"Error en transcripción: {error_str}"}