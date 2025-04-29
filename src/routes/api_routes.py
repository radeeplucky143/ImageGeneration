from fastapi import APIRouter, HTTPException

from src.models.prompt_models import (ApprovalRequest, ImageRequest,
                                      ImageResponse, PromptResponse,
                                      TopicRequest)
from src.services.image_service import ImageService
from src.services.prompt_service import PromptService

router = APIRouter()
prompt_service = PromptService()
image_service = ImageService()

@router.post("/generate-prompts", response_model=PromptResponse)
async def generate_prompts(request: TopicRequest):
    try:
        prompts_dict = await prompt_service.generate_prompts(request.topic, request.num_prompts)
        return PromptResponse(prompts=prompts_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-image", response_model=ImageResponse)
async def generate_image(request: ImageRequest):
    try:
        image_path = await image_service.generate_image(request.prompt_id, request.prompt)
        return ImageResponse(image_path=image_path, prompt_id=request.prompt_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/approve-image")
async def approve_image(request: ApprovalRequest):
    try:
        success = image_service.approve_image(request.prompt_id, request.approved)
        if not success:
            raise HTTPException(status_code=404, detail="Prompt ID not found")
        return {"status": "success", "message": f"Image {request.prompt_id} {'approved' if request.approved else 'rejected'}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 