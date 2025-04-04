import json
import aiohttp
from typing import Dict, List, Any
from utils.config import GPT_API_KEY, GPT_API_URL
from services.news_retrieval import detect_politicians, POLITICIAN_INFO, fetch_articles
from datetime import datetime

async def analyze_politician_claim(text: str, politicians: List[str]) -> Dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {GPT_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Get politician context
    politician_contexts = [POLITICIAN_INFO.get(p, {}) for p in politicians]
    
    system_prompt = {
        "role": "system",
        "content": "You are an expert Filipino fact-checker. Analyze political claims and provide detailed verification."
    }
    
    user_prompt = {
        "role": "user",
        "content": f"""Analyze this claim about politicians {', '.join(politicians)}:
        Claim: {text}
        
        Politician Context:
        {json.dumps(politician_contexts, indent=2)}
        
        Provide:
        1. Is this a verifiable claim? (true/false)
        2. Classification (FALSE/MISLEADING/UNVERIFIED/VERIFIED)
        3. Detailed explanation
        4. Supporting evidence"""
    }
    
    payload = {
        "model": "gpt-3.5-turbo",
        "max_tokens": 1500,
        "messages": [system_prompt, user_prompt],
        "temperature": 0.3
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(GPT_API_URL, headers=headers, json=payload) as response:
            result = await response.json()
            analysis = result["choices"][0]["message"]["content"]
            
            return {
                "is_claim": "true" in analysis.lower(),
                "analysis": analysis
            }

async def get_gpt_fact_check(text: str) -> Dict:
    headers = {
        "Authorization": f"Bearer {GPT_API_KEY}",
        "Content-Type": "application/json"
    }
    
    system_prompt = {
        "role": "system",
        "content": """You are an expert Filipino fact-checker. Format your response exactly like this:
        THIS IS [CLASSIFICATION]!
        [Your clear and concise explanation in a single paragraph, max 1500 characters]
        Sources: 
        1. Source name with URL
        2. Source name with URL
        3. Source name with URL
        
        Note: If classification is UNVERIFIED, explain why:
        - Lack of credible sources
        - Insufficient evidence
        - Ongoing investigation
        - Contradicting information
        - Time-sensitive/outdated information
        
        Use only these classifications: TRUE, FALSE, MISLEADING, UNVERIFIED"""
    }
    
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            system_prompt,
            {"role": "user", "content": f"Fact check this claim: {text}"}
        ],
        "temperature": 0.3,
        "max_tokens": 1500
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(GPT_API_URL, headers=headers, json=payload) as response:
            if response.status != 200:
                return {"status": "error", "message": "Failed to get response from GPT"}
            
            data = await response.json()
            content = data["choices"][0]["message"]["content"]
            
            try:
                # Extract classification and explanation
                lines = content.split('\n')
                classification = None
                explanation = ""
                sources = []
                unverified_reason = ""
                
                for i, line in enumerate(lines):
                    line = line.strip()
                    if '!' in line and not classification:
                        # Look for any of the expected classifications
                        for expected in ['TRUE', 'FALSE', 'MISLEADING', 'UNVERIFIED']:
                            if expected in line:
                                classification = expected
                                # Get the explanation from the next line
                                if i + 1 < len(lines):
                                    explanation = lines[i + 1].strip()
                                break
                    elif line.startswith('Sources:'):
                        # Collect sources
                        sources = [s.strip() for s in lines[i+1:] if s.strip()]
                    elif classification == "UNVERIFIED" and line.startswith('-'):
                        unverified_reason += f"{line}\n"
                
                if not classification:
                    classification = "UNVERIFIED"
                
                return {
                    "status": "success",
                    "classification": classification,
                    "explanation": explanation,
                    "sources": sources,
                    "unverified_reason": unverified_reason.strip(),
                    "analysis": content
                }
            except Exception as e:
                return {
                    "status": "error", 
                    "message": f"Failed to parse response: {str(e)}",
                    "raw_content": content
                }

async def get_gpt_chat_response(message: str, context: str = None) -> str:
    """Handle chat interactions with GPT model"""
    headers = {
        "Authorization": f"Bearer {GPT_API_KEY}",
        "Content-Type": "application/json"
    }
    
    messages = [
        {
            "role": "system",
            "content": "You are an expert Filipino fact-checker assistant helping users understand claims."
        }
    ]
    
    if context:
        messages.append({"role": "user", "content": f"Context: {context}"})
    
    messages.append({"role": "user", "content": message})
    
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(GPT_API_URL, headers=headers, json=payload) as response:
            if response.status != 200:
                return "THIS IS ERROR! Failed to get response."
            data = await response.json()
            return data["choices"][0]["message"]["content"]