import sys
sys.dont_write_bytecode = True
from fastapi import FastAPI
from dotenv import load_dotenv
from src.routes.api_routes import router
from src.config.constants import APIConfig

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title=APIConfig.API_TITLE,
    description=APIConfig.API_DESCRIPTION,
    version=APIConfig.API_VERSION
)

# Include routes
app.include_router(router, prefix=APIConfig.API_PREFIX)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 