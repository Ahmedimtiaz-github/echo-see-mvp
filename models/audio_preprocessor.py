import os
import warnings

# Suppress TF INFO & DEPRECATION messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 0=all, 1=info, 2=warning, 3=error
warnings.filterwarnings('ignore', category=FutureWarning)  # ignore future warnings

import os
import librosa
import soundfile as sf

def validate_and_convert(audio_path, output_folder="./uploads"):
    # Ensure uploads folder exists
    os.makedirs(output_folder, exist_ok=True)

    file_name = os.path.basename(audio_path)
    base, ext = os.path.splitext(file_name)

    out_path = os.path.join(output_folder, base + "_16k.wav")

    # Load audio with original sampling rate
    audio, sr = librosa.load(audio_path, sr=None)

    needs_convert = False

    # Check sample rate
    if sr != 16000:
        needs_convert = True

    # If stereo
    if audio.ndim > 1:
        audio = librosa.to_mono(audio)
        needs_convert = True

    if needs_convert:
        audio_16k = librosa.resample(audio, orig_sr=sr, target_sr=16000)
        sf.write(out_path, audio_16k, 16000)
        return out_path, True
    
    # If no conversion needed, return original path
    return audio_path, False
