import os
from pathlib import Path
from src.config.constants import DirectoryConfig

class PathManager:
    """Manages all project paths and ensures directory structure"""
    
    def __init__(self):
        self.src_dir = DirectoryConfig.SRC
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure all required directories exist"""
        directories = [
            self.src_dir,
            os.path.join(self.src_dir, DirectoryConfig.CONFIG),
            os.path.join(self.src_dir, DirectoryConfig.UTILS),
            os.path.join(self.src_dir, DirectoryConfig.LOGS),
            os.path.join(self.src_dir, DirectoryConfig.IMAGES),
            os.path.join(self.src_dir, DirectoryConfig.PROMPTS),
            os.path.join(self.src_dir, DirectoryConfig.MODELS),
            os.path.join(self.src_dir, DirectoryConfig.ROUTES),
            os.path.join(self.src_dir, DirectoryConfig.SERVICES),
            self.image_ingest_dir,
            self.image_process_dir,
            self.image_approved_dir
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    @property
    def image_ingest_dir(self) -> str:
        return os.path.join(self.src_dir, DirectoryConfig.IMAGES, DirectoryConfig.IMAGE_INGEST)

    @property
    def image_process_dir(self) -> str:
        return os.path.join(self.src_dir, DirectoryConfig.IMAGES, DirectoryConfig.IMAGE_PROCESS)

    @property
    def image_approved_dir(self) -> str:
        return os.path.join(self.src_dir, DirectoryConfig.IMAGES, DirectoryConfig.IMAGE_APPROVED)

    @property
    def prompts_file(self) -> str:
        return DirectoryConfig.PROMPTS_FILE

    @property
    def log_dir(self) -> str:
        return os.path.join(self.src_dir, DirectoryConfig.LOGS)