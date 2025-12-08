from audio_preprocessor import validate_and_convert
from sound_classifier import classify_sound


def process_uploaded_audio(user_audio_path):
    # Step 1: Validate & convert
    formatted_path, converted = validate_and_convert(user_audio_path)

    # Step 2: Send to model
    label, confidence = classify_sound(formatted_path)

    return {
        "converted": converted,
        "audio_used": formatted_path,
        "prediction": label,
        "confidence": round(confidence, 4)
    }


# Example usage
if __name__ == "__main__":
    # Here can add your File path 
    result = process_uploaded_audio("C:\\Users\\BEST LAPTOP\\Desktop\\CodeCelix_Internship\\demo_audio\\dog-barking-406629_16k.wav")
    print(result)
