from loguru import logger

class VoiceService:
    def __init__(self):
        self.enabled = False
        logger.info("Voice service initialized in mock mode")

    async def text_to_speech(self, text: str) -> bytes:
        """Mock text-to-speech conversion"""
        logger.info(f"Mock TTS: {text}")
        return b""  # Return empty bytes for testing

    async def speech_to_text(self, audio_data: bytes) -> str:
        """Mock speech-to-text conversion"""
        logger.info("Mock STT received audio data")
        return "Mock speech recognition result"

    def is_enabled(self) -> bool:
        """Check if voice service is enabled"""
        return self.enabled
