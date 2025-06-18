from fastapi import APIRouter
from typing import Dict, Any
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatMessage(BaseModel):
    message: str

@router.post("/message")
async def send_message(chat_message: ChatMessage) -> Dict[str, Any]:
    """Process a chat message"""
    return {
        "message": "Message received: " + chat_message.message,
        "input": chat_message.message
    }
