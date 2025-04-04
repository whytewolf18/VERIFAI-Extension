from typing import List, Dict

ALLOWED_ORIGINS: List[str] = [
    "chrome-extension://*",
    "http://localhost:*",
    "http://127.0.0.1:*"
]

REMOVED_HEADERS: List[str] = [
    "permissions-policy",
    "content-security-policy",
    "x-content-type-options",
    "x-frame-options"
]

CORS_SETTINGS: Dict = {
    "allow_origins": ALLOWED_ORIGINS,
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"]
}

SECURITY_HEADERS: Dict = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type"
}