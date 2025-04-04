import sys
import importlib
import asyncio
from typing import Dict, Any
import openai
from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from utils.config import get_api_key

def check_dependencies():
    """Check if all required dependencies are installed and importable"""
    dependencies = {
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn',
        'aiohttp': 'aiohttp',
        'openai': 'openai'
    }
    
    missing = []
    for package, import_name in dependencies.items():
        try:
            importlib.import_module(import_name)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("THIS IS ERROR!")
        print("Missing dependencies:", ", ".join(missing))
        print("Please run:")
        print("pip install " + " ".join(missing))
        return False
    return True

# Check dependencies before importing
if not check_dependencies():
    sys.exit(1)

from main import app
from models import GPTModel

# Global model instance
gpt_model = None

async def validate_model():
    """Validate GPT model before starting server"""
    global gpt_model
    
    try:
        print("VALIDATING...")
        api_key = get_api_key()  # Get the API key string
        print(f"API Key type: {type(api_key)}")  # Debug line
        
        if not isinstance(api_key, str):
            print(f"ERROR! API key is not a string, got {type(api_key)}")
            return False
        
        # Print masked version of API key for debugging
        masked_key = f"{api_key[:10]}...{api_key[-4:]}" if api_key else "None"
        print(f"Debug - API Key: {masked_key}")
        
        gpt_model = GPTModel(api_key)  # Pass the string to GPTModel
        
        # Test the model
        test_result = await gpt_model.analyze_text("This is a test claim")
        print(f"Test result: {test_result}")  # Debug line
        
        if isinstance(test_result, dict) and test_result.get("status") == "success":
            print("SUCCESS!")
            return True
        else:
            print(f"ERROR! {test_result.get('message') if isinstance(test_result, dict) else str(test_result)}")
            return False

    except Exception as e:
        print(f"ERROR! {str(e)}")
        return False

# Replace on_event with lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.gpt_model = gpt_model
    yield
    # Shutdown
    app.state.gpt_model = None

# Update FastAPI instance with lifespan
app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    # Initialize and validate model
    if asyncio.run(validate_model()):
        print("STARTING!")
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    else:
        print("ABORTED!")