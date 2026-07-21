"""
Voice Engine supporting Text-to-Speech (TTS) synthesis for Andrew Ng Twin.
"""

import base64
import time
from typing import Dict, Any, Optional
from google.genai import types
from backend.core.config import settings
from backend.core.logger import logger
from backend.llm.gemini_client import GeminiClient


class VoiceService:
    """Manages audio generation for voice interactions."""

    def __init__(self, llm_client: GeminiClient) -> None:
        self.llm = llm_client

    def text_to_speech(self, text: str, voice_name: str = "Puck") -> Dict[str, Any]:
        """
        Converts twin text response into spoken audio bytes using Gemini API config.
        """
        # Dedicated Gemini TTS engine target
        tts_models = [
            "gemini-2.5-flash-preview-tts",
            getattr(settings, "PRIMARY_MODEL", "gemini-2.5-flash")
        ]

        for model_name in tts_models:
            try:
                api_key, key_idx = self.llm._get_available_key()
                client = self.llm._get_client(api_key)

                config = types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name=voice_name
                            )
                        )
                    )
                )

                prompt = (
                    f"Read aloud in a calm, humble, measured, and warm educational tone: {text}"
                )

                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=config,
                )

                audio_data = None
                if response.candidates and response.candidates[0].content.parts:
                    for part in response.candidates[0].content.parts:
                        if hasattr(part, "inline_data") and part.inline_data:
                            audio_data = part.inline_data.data
                            break

                if audio_data:
                    b64_audio = base64.b64encode(audio_data).decode("utf-8")
                    logger.success(f"Native audio generated using model '{model_name}'.")
                    return {
                        "status": "success",
                        "audio_base64": b64_audio,
                        "mime_type": "audio/wav",
                        "model_used": model_name
                    }

            except Exception as e:
                logger.warning(f"TTS generation attempt with '{model_name}' failed: {e}")
                time.sleep(0.5)

        logger.warning("All server-side TTS models unavailable. Falling back to client-side synthesis.")
        return {
            "status": "fallback_client_side",
            "message": "Use Web Speech API client-side synthesis."
        }