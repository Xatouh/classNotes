import whisper
import torch
import sys
import os
import soundfile as sf
import numpy as np
import os
from tqdm import tqdm
import subprocess
from .preProcessFile import preprocess_audio



# Output
output_dir = "output/"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Configuración
MODEL_SIZE = "tiny"  # opciones: tiny, base, small, medium, large, large-v3
USE_FP16 = True       # Usar precisión mixta si tienes GPU compatible (GTX 1650 lo soporta)
LANGUAGE = "en"       # Cambiar a "en", "fr", etc. si es necesario



def STT(audio_path, preprocess=True):
    if not os.path.exists(audio_path):
        print(f"❌ Archivo no encontrado: {audio_path}")
        return
    
    audio_path = notWav(audio_path)  # Verifica si es WAV, si no, lo convierte

    if preprocess:
        print("🔄 Preprocesando audio...")
        audio_path = preprocess_audio(audio_path)
        if not audio_path:
            print("❌ Error al preprocesar el archivo de audio.")
            return
    try:
        # Verifica el dispositivo
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🚀 Usando dispositivo: {device}")

        # Carga del modelo
        model = whisper.load_model(MODEL_SIZE).to(device)
        print(f"🎧 Modelo '{MODEL_SIZE}' cargado")


        # Cargar audio completo para dividirlo
        data, samplerate = sf.read(audio_path)
        duration_sec = len(data) / samplerate
        if duration_sec < 0.5:
            print("⚠️ Audio demasiado corto para transcribir.")
            return
        
        print(f"\n⏱️ Duración del audio: {duration_sec:.2f}s")
        
        # Parámetros de segmentación
        chunk_duration = 30  # segundos (Whisper funciona bien en segmentos de 30s)
        samples_per_chunk = int(samplerate * chunk_duration)
        total_chunks = int(np.ceil(len(data) / samples_per_chunk))

        transcription = ""
        print("🎤 Transcribiendo por segmentos...\n")
        for i in tqdm(range(total_chunks), desc="Progreso", unit="chunk"):

            start_sample = i * samples_per_chunk
            end_sample = min((i + 1) * samples_per_chunk, len(data))
            chunk = data[start_sample:end_sample]

            # Guardar temporalmente el segmento como WAV
            temp_path = f"temp_chunk_{i}.wav"
            sf.write(temp_path, chunk, samplerate)

            # Transcribir
            result = model.transcribe(temp_path, language=LANGUAGE, fp16=USE_FP16 and device == "cuda")
            transcription += result["text"].strip() + " "

            os.remove(temp_path)  # Eliminar archivo temporal


        # Mostrar y guardar transcripción final
        print("\n📝 Transcripción completa:")
        print(f"\n💾 Transcripción guardada.")
        return transcription

    except Exception as e:
        print(f"❌ Error durante la transcripción: {e}")



def wavConversor(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Archivo no encontrado: {path}")
    
    ruta_wav = os.path.splitext(path)[0] + ".wav"
    comando = [
        "ffmpeg", "-y", "-i", path,
        "-ac", "1",             # mono
        "-ar", "16000",         # 16kHz
        ruta_wav
    ]

    try:
        subprocess.run(comando, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"✅ Convertido con ffmpeg: {ruta_wav}")
        return ruta_wav
    except subprocess.CalledProcessError:
        print("❌ Error: ffmpeg no pudo convertir el archivo.")
        return None

def notWav(file):
    if not file.lower().endswith(".wav"):
        print("🔄 Convertiendo archivo a WAV...")
        audio_path = wavConversor(file)
        
        if not audio_path:
            print("❌ Error al convertir el archivo M4A.")
            sys.exit(1)
    else:
        audio_path = file  
    
    return audio_path

# Ejecución por línea de comandos
# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Uso: python transcribe_file.py <archivo_de_audio>")
#     else:
#         file = sys.argv[1]
#         if not file.lower().endswith(".wav"):
#             print("🔄 Convertiendo archivo a WAV...")
#             audio_path = wavConversor(file)
#             if not audio_path:
#                 print("❌ Error al convertir el archivo M4A.")
#                 sys.exit(1)
#         else:
#             audio_path = file
            
#         preprocessed_path = preprocess_audio(audio_path)
#         STT(preprocessed_path)

#         print("🎤 Transcripción completada.")



 