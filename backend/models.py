from transformers import pipeline
from typing import Dict, Any
from openai import AsyncOpenAI

class NLIModel:
    def __init__(self):
        self.model = pipeline("text-classification", model="c:/Users/Denim/OneDrive/Documents/Extension/backend/NLI_model")

    def predict(self, premise, hypothesis):
        return self.model(f"{premise} entails {hypothesis}")

class NLEModel:
    def __init__(self):
        self.model = pipeline("text2text-generation", model="c:/Users/Denim/OneDrive/Documents/Extension/backend/NLE_model")

    def explain(self, text):
        return self.model(text)

class NERModel:
    def __init__(self):
        self.model = pipeline("ner", model="c:/Users/Denim/OneDrive/Documents/Extension/backend/NER_model")

    def recognize(self, text):
        return self.model(text)

class GPTModel:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key is required")
        
        self.client = AsyncOpenAI(api_key=api_key)

    async def analyze_text(self, text: str) -> Dict[str, Any]:
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert Filipino fact-checker."},
                    {"role": "user", "content": f"Analyze this claim: {text}"}
                ],
                max_tokens=1500,
                temperature=0.3
            )
            return {
                "status": "success",
                "analysis": response.choices[0].message.content
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }