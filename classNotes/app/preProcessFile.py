from scipy.signal import butter, lfilter
from pydub import AudioSegment, effects
import numpy as np

def highpass_filter(samples, sample_rate, cutoff=100, order=4):
    nyq = 0.5 * sample_rate
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return lfilter(b, a, samples)

def reduce_noise(samples, noise_profile, alpha=1.0):
    """Simple noise reduction by spectral subtraction"""
    return samples - alpha * noise_profile

def compress(samples, threshold=0.05, ratio=4.0):
    """Basic static compressor"""
    def compress_sample(x):
        if abs(x) < threshold:
            return x
        return np.sign(x) * (threshold + (abs(x) - threshold) / ratio)
    return np.vectorize(compress_sample)(samples)

def normalize(samples):
    return samples / np.max(np.abs(samples))

def preprocess_audio(input_path):
    audio = AudioSegment.from_wav(input_path).set_channels(1)
    samples = np.array(audio.get_array_of_samples()).astype(np.float32)
    sample_rate = audio.frame_rate

    # Normaliza entre -1 y 1
    # print("🔄 Normalizando audio...")
    # samples /= np.max(np.abs(samples))

    # 1. High-pass filter (corte en 100 Hz)
    print("🔄 Aplicando filtro pasa alto...")
    samples = highpass_filter(samples, sample_rate, cutoff=100)

    # 2. Noise profile: primeros 0.5 segundos como ruido
    print("🔄 Reduciendo ruido...")
    noise_duration = int(0.5 * sample_rate)
    noise_profile = samples[:noise_duration]
    noise_profile_mean = np.mean(noise_profile)
    samples = reduce_noise(samples, noise_profile_mean, alpha=1.0)

    # 3. Compresión
    print("🔄 Aplicando compresión dinámica...")
    samples = compress(samples, threshold=0.05, ratio=4.0)

    # 4. Normalización
    print("🔄 Normalizando amplitud...")
    samples = normalize(samples)

    # Exportar como WAV
    print("💾 Exportando audio procesado...")
    processed_audio = AudioSegment(
        (samples * 32767).astype(np.int16).tobytes(),
        frame_rate=sample_rate,
        sample_width=2,
        channels=1
    )
    output_wav = f"{input_path}_pp.wav"
    processed_audio.export(output_wav, format="wav")

    return output_wav