# Image Generation API

A FastAPI-based service for generating and managing AI-generated images using Azure OpenAI.

## Features

- Generate multiple prompts for a given topic
- Generate images from prompts
- Approve/reject generated images
- Automatic organization of images into approved/rejected folders

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in a `.env` file:
```
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_API_VERSION=your_api_version
AZURE_OPENAI_GPT4_DEPLOYMENT=your_gpt4_deployment
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_DALLE_DEPLOYMENT=your_dalle_deployment
```

## Running the API

Start the FastAPI server:
```bash
python app.py
```

The API will be available at `http://localhost:8000`. Access the API documentation at `http://localhost:8000/docs`.

## API Endpoints

### Generate Prompts
- **POST** `/generate-prompts`
- Generates multiple prompts for a given topic
- Request body: `{"topic": "your topic", "num_prompts": 10}`

### Generate Image
- **POST** `/generate-image`
- Generates an image from a prompt
- Request body: `{"prompt_id": "1", "prompt": "your prompt text"}`

### Approve Image
- **POST** `/approve-image`
- Approves or rejects a generated image
- Request body: `{"prompt_id": "1", "approved": true}`

## Project Structure

```
.
├── app.py                 # FastAPI application
├── requirements.txt       # Project dependencies
└── src/
    ├── config/           # Configuration files
    ├── images/           # Generated images
    │   ├── ingest/      # Newly generated images
    │   ├── process/     # Images being processed
    │   └── approved/    # Approved images
    ├── prompts/         # Generated prompts
    ├── utils/           # Utility modules
    │   ├── agent.py     # Azure OpenAI integration
    │   ├── logger.py    # Logging functionality
    │   └── path_manager.py  # File path management
    └── logs/            # Application logs
```

## Configuration

The project can be configured through environment variables or by modifying the constants in `src/config/constants.py`:

- `IMAGE_SIZE`: Size of generated images
- `IMAGE_QUALITY`: Image quality setting
- `IMAGE_STYLE`: Image style setting

## Error Handling

The project includes comprehensive error handling for:
- API connection issues
- Image generation failures
- File system operations
- Invalid user input

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Azure OpenAI Service
- DALL-E 3 for image generation
- Semantic Kernel for AI integration 