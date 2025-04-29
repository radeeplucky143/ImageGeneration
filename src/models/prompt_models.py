from typing import Dict, Optional

from pydantic import BaseModel


class TopicRequest(BaseModel):
    topic: str
    num_prompts: int = 10

class PromptInfo(BaseModel):
    prompt: str
    approved: bool
    image_path: Optional[str] = None
    status: str
    created_at: str
    topic: str

class PromptResponse(BaseModel):
    prompts: Dict[str, PromptInfo]

class ImageRequest(BaseModel):
    prompt_id: str
    prompt: str

class ImageResponse(BaseModel):
    image_path: str
    prompt_id: str

class ApprovalRequest(BaseModel):
    prompt_id: str
    approved: bool 