from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from loguru import logger

from app.core.config import get_settings
from app.core.security import verify_password, get_password_hash
from app.services.nlp_service import NLPService
from app.services.voice_service import VoiceService
from app.services.system_service import SystemService
from app.services.pentest_service import PentestService
from app.services.docker_service import DockerService

# Security
security = HTTPBearer()

# Mock user database (replace with real database in production)
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": get_password_hash("admin123"),
        "role": "admin",
        "permissions": ["read", "write", "execute", "admin"]
    },
    "user": {
        "username": "user",
        "hashed_password": get_password_hash("user123"),
        "role": "user",
        "permissions": ["read"]
    }
}

def authenticate_user(username: str, password: str):
    """Authenticate user credentials"""
    user = fake_users_db.get(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    settings = get_settings()
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        settings = get_settings()
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: dict = Depends(get_current_user)):
    """Get current active user"""
    return current_user

def require_permission(permission: str):
    """Decorator to require specific permission"""
    def permission_checker(current_user: dict = Depends(get_current_active_user)):
        if permission not in current_user.get("permissions", []):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return permission_checker

# Service dependencies
def get_nlp_service() -> NLPService:
    """Get NLP service instance"""
    return NLPService()

def get_voice_service() -> VoiceService:
    """Get Voice service instance"""
    return VoiceService()

def get_system_service() -> SystemService:
    """Get System service instance"""
    return SystemService(get_settings())

def get_pentest_service() -> PentestService:
    """Get Pentest service instance"""
    return PentestService(get_settings())

def get_docker_service() -> DockerService:
    """Get Docker service instance"""
    return DockerService()
