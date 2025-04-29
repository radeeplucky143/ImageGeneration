import os
from dotenv import load_dotenv

load_dotenv()

class DirectoryConfig:
    """Directory Configuration"""
    # Use /tmp as the base directory for Vercel compatibility
    BASE = '/tmp'
    SRC = os.path.join(BASE, 'src')
    CONFIG = 'config'
    UTILS = 'utils'
    LOGS = 'logs'
    IMAGES = 'images'
    PROMPTS = 'prompts'
    MODELS = 'models'
    ROUTES = 'routes'
    SERVICES = 'services'
    
    # Image subdirectories
    IMAGE_INGEST = 'ingest'
    IMAGE_PROCESS = 'process'
    IMAGE_APPROVED = 'approved'
    
    # File paths
    PROMPTS_FILE = os.path.join(SRC, PROMPTS, 'prompts.json')

class AzureConfig:
    """Azure OpenAI Configuration"""
    API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
    API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION")
    GTP4_DEPLOYMENT = os.environ.get("AZURE_OPENAI_GPT4_DEPLOYMENT")
    ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
    EMBEDDING_DEPLOYMENT = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    DALL_E_DEPLOYMENT = os.environ.get("AZURE_OPENAI_DALLE_DEPLOYMENT")
    
class ImageConfig:
    """Image Generation Configuration"""
    IMAGE_SIZE = os.environ.get("IMAGE_SIZE", "1024x1024")
    IMAGE_QUALITY = os.environ.get("IMAGE_QUALITY", "standard")
    IMAGE_STYLE = os.environ.get("IMAGE_STYLE", "natural")

class APIConfig:
    """API Configuration"""
    API_PREFIX = "/api/v1"
    API_TITLE = "Image Generation API"
    API_DESCRIPTION = "API for generating and managing AI-generated images"
    API_VERSION = "1.0.0"

class GITConfig:
    """GIT Configuration"""
    GITKEEP = '.gitkeep' 