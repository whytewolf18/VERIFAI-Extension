import re
import spacy
from models import NERModel

try:
    nlp = spacy.load("en_core_web_sm")
except:
    nlp = None

ner_model = NERModel()

def detect_claim(text):
    """
    Detects claims in English text while maintaining awareness of Filipino context.
    Returns True if a claim is detected; otherwise, False.
    """
    # English-focused claim patterns
    claim_patterns = [
        r"(claims that|states that|alleges that)",
        r"(according to|says that|believes that)",
        r"(it is true that|it is false that)",
        r"(reports indicate|sources say|experts say)"
    ]
    
    # Patterns for implicit claims
    implicit_patterns = [
        r"(always|never|all|none|every|no one)",
        r"(definitely|absolutely|certainly|undoubtedly)",
        r"(best|worst|most|least)",
        r"(will|would|should|must|need to)"
    ]
    
    # Check patterns
    for pattern in claim_patterns + implicit_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    
    # Use NLP if available
    if nlp:
        doc = nlp(text)
        
        # Check for factual verbs
        factual_verbs = ["prove", "demonstrate", "show", "confirm", "verify", "establish"]
        
        for token in doc:
            if token.lemma_ in factual_verbs:
                return True
            
        # Check for subject + modal verb + verb pattern
        for token in doc:
            if token.dep_ == "nsubj" and token.head.pos_ == "VERB":
                for child in token.head.children:
                    if child.pos_ == "AUX" and child.tag_ == "MD":
                        return True
    
    # Use NER model to detect entities
    entities = ner_model.recognize(text)
    if entities:
        return True
    
    return False