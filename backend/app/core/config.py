from pydantic import BaseSettings
from typing import Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # Application settings
    APP_NAME: str = "Windows Server Assistant"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./windows_assistant.db"
    
    # API Keys (stored securely in environment variables)
    OPENAI_API_KEY: Optional[str] = None
    DEEPSEEK_API_KEY: Optional[str] = None
    AZURE_SPEECH_KEY: Optional[str] = None
    AZURE_SPEECH_REGION: Optional[str] = None
    
    # Penetration Testing Tool Settings
    OWASP_ZAP_URL: str = "http://localhost:8080"
    BURP_SUITE_URL: str = "http://localhost:1337"
    ACUNETIX_URL: Optional[str] = None
    SONARQUBE_URL: Optional[str] = None
    
    # Docker settings
    DOCKER_HOST: Optional[str] = None
    
    # Windows specific settings
    POWERSHELL_EXECUTION_POLICY: str = "RemoteSigned"
    CHOCOLATEY_PATH: str = "C:\\ProgramData\\chocolatey\\bin\\choco.exe"
    WINGET_PATH: str = "winget"
    
    # Additional penetration testing tool settings
    ZAP_API_KEY: Optional[str] = None
    ZAP_HOST: str = "localhost"
    ZAP_PORT: int = 8080
    NMAP_PATH: str = "nmap"
    METASPLOIT_PATH: str = "msfconsole"
    BURP_API_KEY: Optional[str] = None
    BURP_HOST: str = "localhost"
    BURP_PORT: int = 1337
    
    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/windows_assistant.log"
    
    # Security settings
    REQUIRE_CONFIRMATION_FOR_PRIVILEGED: bool = True
    MAX_COMMAND_TIMEOUT: int = 300  # 5 minutes
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()

def get_settings() -> Settings:
    """Get application settings"""
    return settings

def validate_configuration():
    """Validate critical configuration settings"""
    errors = []
    
    if not settings.SECRET_KEY or settings.SECRET_KEY == "your-secret-key-change-in-production":
        errors.append("SECRET_KEY must be set to a secure value")
    
    if not settings.OPENAI_API_KEY and not settings.DEEPSEEK_API_KEY:
        errors.append("At least one NLP API key (OPENAI_API_KEY or DEEPSEEK_API_KEY) must be configured")
    
    # Check if required paths exist
    log_dir = Path(settings.LOG_FILE).parent
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)
    
    if errors:
        raise ValueError(f"Configuration errors: {'; '.join(errors)}")
    
    return True
