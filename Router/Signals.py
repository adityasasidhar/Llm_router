from dataclasses import dataclass
from typing import Literal
import json
from pathlib import Path

@dataclass
class Signal:
    tokens : int
    reasoning : bool
    latency : Literal["low", "medium", "high"]
    multimodal : bool
    safety_score : float

# Load keywords from JSON file
_words_path = Path(__file__).parent / "words.json"
with open(_words_path, "r") as f:
    _keywords = json.load(f)

def extract_signal(query: str, multimodal: bool) -> Signal:
    """Extract signal characteristics from a query."""
    words = query.split()
    tokens = int(len(words) * 1.5)
    
    query_lower = query.lower()
    
    # Check for reasoning keywords
    reasoning = any(keyword in query_lower for keyword in _keywords["reasoning"])
    
    # Determine latency requirements
    latency = "medium"
    if any(k in query_lower for k in _keywords["low_latency"]):
        latency = "low"
    elif any(k in query_lower for k in _keywords["high_latency"]):
        latency = "high"
    
    # Check safety
    if any(word in query_lower for word in _keywords["unsafe"]):
        safety_score = 0.1
    else:
        safety_score = 0.95

    return Signal(
        tokens=tokens,
        reasoning=reasoning,
        latency=latency,
        multimodal=multimodal,
        safety_score=safety_score
    )
