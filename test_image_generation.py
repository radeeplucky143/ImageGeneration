import asyncio
from src.utils.agent import AzureOpenAIChat
from src.utils.logger import logger

async def test_image_generation():
    """Test image generation with a sample prompt"""
    try:
        # Initialize the agent
        agent = AzureOpenAIChat()
        
        # Sample prompt
        prompt = "A serene landscape with a mountain lake at sunset, surrounded by pine trees, in a photorealistic style"
        
        logger.info("Starting image generation test...")
        logger.info(f"Using prompt: {prompt}")
        logger.info(f"Using deployment: {agent.dall_e_deployment}")
        logger.info(f"Using API version: {agent.api_version}")
        
        # Generate the image
        image_path = await agent.generate_image(prompt)
        
        logger.info(f"Image generated successfully at: {image_path}")
        return image_path
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(test_image_generation()) 