import asyncio
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Union

import aiohttp
from openai import AzureOpenAI
from PIL import Image
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion, AzureTextEmbedding
from semantic_kernel.memory import VolatileMemoryStore

from src.config.constants import AzureConfig, ImageConfig
from src.utils.logger import logger
from src.utils.path_manager import PathManager


class AzureOpenAIChat:
    """Azure OpenAI Chat agent for generating images and prompts."""
    
    def __init__(self, max_retries: int = 3, timeout: int = 30):
        """
        Initialize the Azure OpenAI Chat agent.
        
        Args:
            max_retries (int): Maximum number of retries for API calls
            timeout (int): Timeout in seconds for API calls
        """
        self._validate_config()
        
        self.api_key = AzureConfig.API_KEY
        self.endpoint = AzureConfig.ENDPOINT
        self.deployment = AzureConfig.GTP4_DEPLOYMENT
        self.api_version = "2024-02-15-preview"  # Updated API version for DALL-E 3
        self.embedding_deployment = AzureConfig.EMBEDDING_DEPLOYMENT
        self.dall_e_deployment = AzureConfig.DALL_E_DEPLOYMENT
        
        self.max_retries = max_retries
        self.timeout = timeout
        self.path_manager = PathManager()
        
        self.kernel = self._initialize_kernel()
        self.memory = VolatileMemoryStore()
        self.client = self._initialize_client()
        
    def _initialize_client(self) -> AzureOpenAI:
        """Initialize the Azure OpenAI client"""
        return AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.endpoint,
            timeout=self.timeout
        )

    def _validate_config(self) -> None:
        """Validate the configuration settings."""
        required_vars = [
            'API_KEY', 'ENDPOINT', 'GTP4_DEPLOYMENT', 'API_VERSION',
            'EMBEDDING_DEPLOYMENT', 'DALL_E_DEPLOYMENT'
        ]
        
        for var in required_vars:
            if not getattr(AzureConfig, var):
                raise ValueError(f"Missing required configuration: {var}")
    
    def _initialize_kernel(self) -> Kernel:
        """Initialize the Semantic Kernel with Azure services."""
        kernel = Kernel()
        kernel.add_service(
            AzureChatCompletion(
                deployment_name=self.deployment,
                endpoint=self.endpoint,
                api_key=self.api_key,
                api_version=self.api_version
            )
        )
        kernel.add_service(
            AzureTextEmbedding(
                deployment_name=self.embedding_deployment,
                endpoint=self.endpoint,
                api_key=self.api_key,
                api_version=self.api_version
            )
        )
        return kernel

    async def _download_image(self, url: str, save_path: Union[str, Path]) -> None:
        """
        Download an image from a URL and save it to the specified path.
        
        Args:
            url (str): URL of the image to download
            save_path (Union[str, Path]): Path to save the image
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise ValueError(f"Failed to download image: {response.status}")
                
                with open(save_path, "wb") as f:
                    f.write(await response.read())
    
    def _validate_image(self, image_path: Union[str, Path]) -> None:
        """
        Validate the downloaded image.
        
        Args:
            image_path (Union[str, Path]): Path to the image file
        """
        try:
            with Image.open(image_path) as img:
                if img.format not in ['PNG', 'JPEG']:
                    raise ValueError(f"Unsupported image format: {img.format}")
                
                width, height = img.size
                if width < 256 or height < 256:
                    raise ValueError(f"Image too small: {width}x{height}")
        except Exception as e:
            raise ValueError(f"Invalid image file: {str(e)}")

    async def generate_image(self, prompt: str, save_path: Optional[Union[str, Path]] = None) -> str:
        """
        Generate an image using DALL-E 3 and save it to the specified path.
        
        Args:
            prompt (str): The prompt to generate the image from
            save_path (Optional[Union[str, Path]]): Path to save the image
            
        Returns:
            str: Path to the saved image
            
        Raises:
            ValueError: If the prompt is invalid or image generation fails
            Exception: For other errors during image generation
        """
        if not prompt or len(prompt.strip()) < 10:
            raise ValueError("Prompt must be at least 10 characters long")
        
        try:
            logger.info(f"Generating image for prompt: {prompt}")
            
            for attempt in range(self.max_retries):
                try:
                    response = self.client.images.generate(
                        model=self.dall_e_deployment,
                        prompt=prompt,
                        n=1,
                        size=ImageConfig.IMAGE_SIZE,
                        quality=ImageConfig.IMAGE_QUALITY,
                        style=ImageConfig.IMAGE_STYLE
                    )
                    break
                except Exception as e:
                    if attempt == self.max_retries - 1:
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                    await asyncio.sleep(2 ** attempt)
            
            if not response.data:
                raise ValueError("No image data received from API")
            
            image_url = response.data[0].url
            if not image_url:
                raise ValueError("No image URL in response")
            
            # Generate save path if not provided
            if save_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"image_{timestamp}.png"
                save_path = os.path.join(self.path_manager.image_ingest_dir, filename)
            
            # Download and validate the image
            await self._download_image(image_url, save_path)
            self._validate_image(save_path)
            
            logger.info(f"Image generated and saved to: {save_path}")
            return str(save_path)
            
        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            raise

    async def generate_prompts(self, topic: str, n: int = 10) -> List[str]:
        """
        Generate a list of creative prompts for a given topic.
        
        Args:
            topic (str): The topic to generate prompts for
            n (int): Number of prompts to generate
            
        Returns:
            List[str]: List of generated prompts
            
        Raises:
            ValueError: If the topic is invalid or prompt generation fails
        """
        if not topic or len(topic.strip()) < 3:
            raise ValueError("Topic must be at least 3 characters long")
        
        if n < 1 or n > 20:
            raise ValueError("Number of prompts must be between 1 and 20")
        
        try:
            system_prompt = (
                f"You are a creative prompt generator for DALL-E. Given the topic '{topic}', "
                f"generate {n} unique, detailed, and imaginative prompts for image generation. "
                f"Each prompt should be descriptive and specific. "
                f"Return only the list of prompts, one per line, no numbering or extra text."
            )
            
            for attempt in range(self.max_retries):
                try:
                    response = self.client.chat.completions.create(
                        model=self.deployment,
                        messages=[
                            {"role": "system", "content": system_prompt},
                        ],
                        max_tokens=500,
                        temperature=0.9,
                        timeout=self.timeout
                    )
                    break
                except Exception as e:
                    if attempt == self.max_retries - 1:
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                    await asyncio.sleep(2 ** attempt)
            
            prompts_text = response.choices[0].message.content.strip()
            prompts = [p.strip() for p in prompts_text.split("\n") if p.strip()]
            
            if len(prompts) < n:
                logger.warning(f"Generated only {len(prompts)} prompts instead of {n}")
            
            return prompts[:n]
            
        except Exception as e:
            logger.error(f"Error generating prompts: {str(e)}")
            raise 