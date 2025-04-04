# ui_highlighter.py - Enhanced claim highlighting with Filipino language support
from services.llm_service import get_gpt_fact_check, analyze_politician_claim  # Changed import
from services.news_retrieval import detect_politicians
import re

async def highlight_claims(text):
    """
    Processes text, detects claims, and applies colored underlines based on fact-checking results.
    Supports both English and Filipino text.
    Returns highlighted HTML and a list of annotations.
    """
    # Define color mapping for labels
    label_colors = {
        "FALSE": "red",
        "MISLEADING": "orange",
        "UNFOUNDED": "blue",
        "VERIFIED": "green",
        "ERROR": "gray"
    }
    
    try:
        # First detect politicians
        mentioned_politicians = detect_politicians(text)
        if not mentioned_politicians:
            return {
                "status": "no_politicians",
                "message": "No politicians mentioned in text",
                "highlighted_html": text,
                "annotations": []
            }

        # Check if it's a claim
        claim_analysis = await analyze_politician_claim(text, mentioned_politicians)
        if not claim_analysis["is_claim"]:
            return {
                "status": "no_claim",
                "message": "No political claim detected",
                "highlighted_html": text,
                "annotations": []
            }

        # Get fact check analysis
        analysis = await get_gpt_fact_check(text)
        if analysis["status"] != "success":
            return {
                "status": "error",
                "message": analysis.get("message", "Analysis failed"),
                "highlighted_html": text,
                "annotations": []
            }

        # Create highlighted version with annotations
        classification = analysis["analysis"]["classification"]
        color = label_colors.get(classification, "gray")
        
        return {
            "status": "success",
            "highlighted_html": f'<span class="underline-{color}">{text}</span>',
            "annotations": [{
                "text": text,
                "classification": classification,
                "explanation": analysis["analysis"]["explanation"],
                "evidence": analysis["analysis"]["evidence"],
                "sources": analysis["analysis"]["sources"],
                "color": color
            }]
        }

    except Exception as e:
        print(f"Error in highlight_claims: {str(e)}")
        return {
            "status": "error",
            "message": str(e),
            "highlighted_html": text,
            "annotations": []
        }