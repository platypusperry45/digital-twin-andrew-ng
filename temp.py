"""
Test script for Gemini Voice Synthesis.
"""
from backend.core.container import container
from backend.services.voice_service import VoiceService

def test_voice():
    print("Initializing Voice Service...")
    voice_service = VoiceService(llm_client=container.llm)
    
    sample_text = "Hello! Let's build some intuition about deep learning today."
    print(f"Generating TTS for: '{sample_text}'")
    
    result = voice_service.text_to_speech(text=sample_text, voice_name="Puck")
    
    print("\nResult Status:", result.get("status"))
    if result.get("status") == "success":
        print("MIME Type:", result.get("mime_type"))
        print("Audio Base64 length:", len(result.get("audio_base64", "")))
        print("Sample snippet:", result.get("audio_base64")[:50] + "...")
    else:
        print("Fallback message:", result.get("message"))

if __name__ == "__main__":
    test_voice()