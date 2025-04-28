import os
import json
from datetime import datetime
from typing import Dict
from src.utils.agent import AzureOpenAIChat
from src.utils.path_manager import PathManager

class PromptService:
    def __init__(self):
        self.path_manager = PathManager()
        self.agent = AzureOpenAIChat()

    def load_prompts(self) -> Dict:
        """Load prompts from the JSON file"""
        if not os.path.exists(self.path_manager.prompts_file):
            return {}
        with open(self.path_manager.prompts_file, 'r') as f:
            return json.load(f)

    def save_prompts(self, prompts: Dict):
        """Save prompts to the JSON file"""
        with open(self.path_manager.prompts_file, 'w') as f:
            json.dump(prompts, f, indent=4)

    async def generate_prompts(self, topic: str, num_prompts: int = 10) -> Dict:
        """Generate new prompts for a topic"""
        prompts = await self.agent.generate_prompts(topic, n=num_prompts)
        prompts_dict = self.load_prompts()
        
        # Get the next available ID
        next_id = str(max([int(k) for k in prompts_dict.keys()] + [0]) + 1)
        
        # Add new prompts to the dictionary
        for idx, prompt in enumerate(prompts, int(next_id)):
            prompts_dict[str(idx)] = {
                "prompt": prompt,
                "approved": False,
                "image_path": None,
                "status": "pending",
                "created_at": datetime.now().isoformat(),
                "topic": topic
            }
        
        self.save_prompts(prompts_dict)
        return prompts_dict

    def update_prompt_status(self, prompt_id: str, status: str, image_path: str = None):
        """Update the status of a prompt"""
        prompts_dict = self.load_prompts()
        if prompt_id in prompts_dict:
            prompts_dict[prompt_id]["status"] = status
            if image_path:
                prompts_dict[prompt_id]["image_path"] = image_path
            self.save_prompts(prompts_dict) 