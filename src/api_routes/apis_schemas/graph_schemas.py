from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class UserMessage(BaseModel):
    content: str
    thread_id: Optional[str] = None


class ChatResponse(BaseModel):
    thread_id: str
    response: str
    full_state: Dict[str, Any]
