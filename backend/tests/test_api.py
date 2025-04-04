import os
import sys
from pathlib import Path
import requests

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from services.llm_service import analyze_politician_claim, get_gpt_fact_check
import json

# Define the API endpoint
url = "http://localhost:8000/verify"

# Define the claim to be analyzed
claim = "President Duterte claims that the Philippines has one of the lowest COVID-19 infection rates in the world."

# Define the payload
payload = {
    "text": claim,
    "language": "en"
}

# Send the request to the API
response = requests.post(url, json=payload)

# Print the response
print(response.json())

def test_analysis():
    text = "BBM claims that the Philippines will be the next Asian tiger economy"
    politicians = ["Ferdinand Marcos Jr."]
    
    print("Testing politician claim analysis...")
    is_claim = analyze_politician_claim(text, politicians)
    print(f"Is claim: {is_claim}")
    
    if is_claim:
        print("\nGetting fact check analysis...")
        analysis = get_gpt_fact_check(text)
        print(json.dumps(analysis, indent=2))

if __name__ == "__main__":
    test_analysis()