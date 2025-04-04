import json
import aiohttp
from typing import Dict
from utils.config import GPT_API_KEY, GPT_API_URL

async def generate_sources_gpt(claim: str) -> Dict:
    """Generate sources and evidence using GPT when Google Search fails"""
    headers = {
        "Authorization": f"Bearer {GPT_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are an expert Filipino fact-checker and researcher."},
            {"role": "user", "content": f"Provide sources and evidence for the following claim: {claim}"}
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(GPT_API_URL, headers=headers, json=payload) as response:
            if response.status != 200:
                return {"status": "error", "message": "Failed to fetch GPT response"}
            data = await response.json()
            return {"status": "success", "sources": data["choices"][0]["message"]["content"]}