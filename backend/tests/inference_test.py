import sys
from pathlib import Path
import json
import time
from datetime import datetime
from typing import Dict, List

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

from services.llm_service import analyze_politician_claim, get_gpt_fact_check
from services.news_retrieval import detect_politicians, fetch_articles
from services.google_service import google_search
from utils.config import validate_api_key

class TestResult:
    def __init__(self):
        self.text: str = ""
        self.politicians: List[str] = []
        self.is_claim: bool = False
        self.analysis: Dict = {}
        self.evidence: Dict = {
            "official_sources": [],
            "news_results": [],
            "fact_checks": []
        }
        self.processing_time: float = 0.0

def test_inference():
    test_cases = [
        "BBM claims Philippines achieved 6.9% GDP growth in 2023",
        "Sara Duterte announces mandatory ROTC implementation",
        "GMA claims 8% economic growth target for 2024",
        "According to Imee Marcos, agriculture needs ₱200B funding"
    ]
    
    results = []
    total_start = time.time()
    
    print("\n=== Starting Enhanced Inference Tests ===\n")
    
    for test_case in test_cases:
        result = TestResult()
        result.text = test_case
        case_start = time.time()
        
        try:
            print(f"Testing: '{test_case}'")
            print("-" * 50)
            
            # Step 1: Detect politicians
            result.politicians = detect_politicians(test_case)
            print(f"Detected politicians: {result.politicians}")
            
            if result.politicians:
                # Step 2: Check if it's a claim
                result.is_claim = analyze_politician_claim(test_case, result.politicians)
                print(f"Is claim: {result.is_claim}")
                
                if result.is_claim:
                    # Step 3: Fetch supporting evidence first
                    print("\nGathering evidence...")
                    result.evidence = fetch_articles(test_case)
                    
                    # Print evidence summary
                    sources_found = (
                        len(result.evidence.get("official_sources", [])) +
                        len(result.evidence.get("news_results", [])) +
                        len(result.evidence.get("fact_checks", []))
                    )
                    print(f"\nFound {sources_found} relevant sources:")
                    
                    # Show official sources
                    if result.evidence.get("official_sources"):
                        print("\n📊 Official Sources:")
                        for idx, source in enumerate(result.evidence["official_sources"][:2], 1):
                            print(f"{idx}. {source.get('title', 'No title')}")
                            print(f"   URL: {source.get('link', 'No link')}")
                            print(f"   Date: {source.get('date_published', 'No date')}\n")
                    
                    # Show news articles
                    if result.evidence.get("news_results"):
                        print("\n📰 News Articles:")
                        for idx, article in enumerate(result.evidence["news_results"][:3], 1):
                            print(f"{idx}. {article.get('title', 'No title')}")
                            print(f"   URL: {article.get('link', 'No link')}")
                            print(f"   Date: {article.get('date_published', 'No date')}\n")
                    
                    # Show fact checks
                    if result.evidence.get("fact_checks"):
                        print("\n✓ Fact Checks:")
                        for idx, check in enumerate(result.evidence["fact_checks"][:2], 1):
                            print(f"{idx}. {check.get('claim', 'No claim')}")
                            print(f"   Verdict: {check.get('verdict', 'No verdict')}")
                            print(f"   URL: {check.get('link', 'No link')}")
                            print(f"   Date: {check.get('date', 'No date')}\n")
                    
                    # Step 4: Get AI analysis with gathered evidence
                    print("\nGenerating analysis...")
                    result.analysis = get_gpt_fact_check(test_case)
                    print("\nAI Analysis:")
                    print(json.dumps(result.analysis, indent=2))
            
            result.processing_time = time.time() - case_start
            print(f"\nProcessing time: {result.processing_time:.2f} seconds")
            results.append(result.__dict__)
            
        except Exception as e:
            print(f"Error processing case: {str(e)}")
            continue
            
        print("-" * 50 + "\n")
    
    # Generate summary
    total_time = time.time() - total_start
    summary = {
        "total_cases": len(test_cases),
        "successful_cases": len(results),
        "total_time": f"{total_time:.2f} seconds",
        "average_time_per_case": f"{total_time/len(test_cases):.2f} seconds"
    }
    
    # Save results
    output = {
        "timestamp": datetime.now().isoformat(),
        "results": results,
        "summary": summary
    }
    
    output_file = Path(__file__).parent / "inference_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    
    print("\n=== Test Summary ===")
    print(json.dumps(summary, indent=2))
    print(f"\nDetailed results saved to: {output_file}")

if __name__ == "__main__":
    test_inference()