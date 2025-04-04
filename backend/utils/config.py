import os
import requests
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_api_key() -> str:
    """Validate and return OpenAI API key"""
    api_key = os.getenv('OPENAI_API_KEY')
    print(f"Raw API key type: {type(api_key)}")  # Debug line
    
    if not isinstance(api_key, str):
        raise ValueError(f"API key must be a string, got {type(api_key)}")
    
    if not api_key.startswith('sk-'):
        raise ValueError("Invalid OpenAI API key format - must start with 'sk-'")
    
    print("✓ API key is valid")
    return api_key

def validate_api_key(verbose: bool = True) -> bool:
    """
    Validate OpenAI API key by making an API call
    Args:
        verbose: Whether to print status messages
    Returns:
        bool: True if key is valid, False otherwise
    """
    try:
        session = requests.Session()
        response = session.get(
            "https://api.openai.com/v1/models",
            headers={"Authorization": f"Bearer {GPT_API_KEY}"}
        )
        
        if response.status_code == 200:
            if verbose:
                print("✓ API key is valid")
            return True
        
        if response.status_code == 401:
            if verbose:
                print("✗ Invalid API key or unauthorized access")
                print("Please check your OpenAI account and billing status")
            return False
        
        if verbose:
            print(f"✗ API error: {response.status_code} - {response.text}")
        return False
        
    except requests.exceptions.RequestException as e:
        if verbose:
            print(f"✗ Connection error: {str(e)}")
        return False

# API Configuration
GPT_API_KEY = get_api_key()
GPT_API_URL = "https://api.openai.com/v1/chat/completions"
GPT_MODEL = "gpt-3.5-turbo"  # Updated to valid model name
GPT_TIMEOUT = 10  # seconds

# Add proxy settings if needed
PROXY_CONFIG = {
    'http': os.getenv('HTTP_PROXY'),
    'https': os.getenv('HTTPS_PROXY')
}

# Google Search Configuration
GOOGLE_API_KEYS = [
    os.getenv("GOOGLE_API_KEY_1"),
    os.getenv("GOOGLE_API_KEY_2"),
    os.getenv("GOOGLE_API_KEY_3"),
    os.getenv("GOOGLE_API_KEY_4"),
    os.getenv("GOOGLE_API_KEY_5")
]

if not any(GOOGLE_API_KEYS):
    raise ValueError("At least one GOOGLE_API_KEY environment variable must be set")

GOOGLE_SEARCH_CX = os.getenv("GOOGLE_SEARCH_CX")
if not GOOGLE_SEARCH_CX:
    raise ValueError("GOOGLE_SEARCH_CX environment variable is not set")

GOOGLE_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"

# Filipino Source Configuration
SOURCE_CONFIG = {
    "government": {
        "officialgazette": {
            "domain": "officialgazette.gov.ph",
            "prefix": "www",
            "pattern": "www.officialgazette.gov.ph/*"
        },
        "comelec": {
            "domain": "comelec.gov.ph",
            "prefix": "*",
            "pattern": "*.comelec.gov.ph/*"
        },
        "psa": {
            "domain": "psa.gov.ph",
            "prefix": "*",
            "pattern": "*.psa.gov.ph/*"
        }
    },
    "news": {
        "inquirer": {
            "domain": "inquirer.net",
            "prefix": "newsinfo",
            "pattern": "newsinfo.inquirer.net/*"
        },
        "gmanews": {
            "domain": "gmanetwork.com",
            "prefix": "www",
            "pattern": "www.gmanetwork.com/news/*"
        },
        "cnn": {
            "domain": "cnn.com",
            "prefix": "edition",
            "pattern": "edition.cnn.com/*"
        },
        "mb": {
            "domain": "mb.com.ph",
            "prefix": "*",
            "pattern": "*.mb.com.ph/*"
        },
        "philstar": {
            "domain": "philstar.com",
            "prefix": "www",
            "pattern": "www.philstar.com/*"
        },
        "rappler": {
            "domain": "rappler.com",
            "prefix": "www",
            "pattern": "www.rappler.com/philippines*"
        },
        "abscbn": {
            "domain": "abs-cbn.com",
            "prefix": "www",
            "pattern": "www.abs-cbn.com/*"
        }
    },
    "factcheck": {
        "verafiles": {
            "domain": "verafiles.org",
            "prefix": "www",
            "pattern": "www.verafiles.org/fact-check/*"
        },
        "tsek": {
            "domain": "tsek.ph",
            "prefix": "www",
            "pattern": "www.tsek.ph/*"
        },
        "afp": {
            "domain": "factcheck.afp.com",
            "prefix": None,
            "pattern": "factcheck.afp.com/philippines/*"
        }
    }
}

# Helper functions for source management
def get_source_domains(source_type: str) -> List[str]:
    """Get all domains for a specific source type"""
    if source_type not in SOURCE_CONFIG:
        raise ValueError(f"Invalid source type: {source_type}")
    return [f"site:{info['domain']}" for info in SOURCE_CONFIG[source_type].values()]

def get_source_patterns(source_type: str) -> List[str]:
    """Get all URL patterns for a specific source type"""
    if source_type not in SOURCE_CONFIG:
        raise ValueError(f"Invalid source type: {source_type}")
    return [info['pattern'] for info in SOURCE_CONFIG[source_type].values()]

# Maintain backward compatibility
FILIPINO_FACTCHECK_SITES = get_source_domains("factcheck")
FILIPINO_NEWS_SITES = get_source_domains("news")

# Search Settings
SEARCH_SETTINGS = {
    "max_results": 10,
    "min_request_interval": 0.5,  # seconds
    "request_timeout": 30,  # seconds
    "max_retries": 3
}