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
    "allow_methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Accept", "Origin"],
    "expose_headers": ["Content-Length", "Content-Type"]
}

SECURITY_HEADERS: Dict = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Accept, Origin",
    "Access-Control-Max-Age": "3600"
}