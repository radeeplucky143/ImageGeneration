import os
import shutil
from datetime import datetime

from src.config.constants import ImageConfig
from src.services.prompt_service import PromptService
from src.utils.agent import AzureOpenAIChat
from src.utils.path_manager import PathManager


class ImageService:
    def __init__(self):
        self.path_manager = PathManager()
        self.agent = AzureOpenAIChat()
        self.prompt_service = PromptService()

    async def generate_image(self, prompt_id: str, prompt: str) -> str:
        """Generate an image from a prompt"""
        # Generate image and save to ingest folder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        raw_image_path = os.path.join(self.path_manager.image_ingest_dir, f'image_{prompt_id}_{timestamp}.png')
        
        # Use image configuration from constants
        image_path = await self.agent.generate_image(
            prompt, 
            save_path=str(raw_image_path),
            size=ImageConfig.IMAGE_SIZE,
            quality=ImageConfig.IMAGE_QUALITY,
            style=ImageConfig.IMAGE_STYLE
        )
        
        # Update prompt status
        self.prompt_service.update_prompt_status(prompt_id, "generated", image_path)
        
        return image_path

    def approve_image(self, prompt_id: str, approved: bool) -> bool:
        """Approve or reject an image"""
        prompts_dict = self.prompt_service.load_prompts()
        
        if prompt_id not in prompts_dict:
            return False
        
        # Update approval status
        prompts_dict[prompt_id]["approved"] = approved
        prompts_dict[prompt_id]["status"] = "approved" if approved else "rejected"
        
        # If approved, move the image to approved folder
        if approved and prompts_dict[prompt_id]["image_path"]:
            current_path = prompts_dict[prompt_id]["image_path"]
            filename = os.path.basename(current_path)
            new_path = os.path.join(self.path_manager.image_approved_dir, filename)
            shutil.move(current_path, new_path)
            prompts_dict[prompt_id]["image_path"] = new_path
        
        self.prompt_service.save_prompts(prompts_dict)
        return True 