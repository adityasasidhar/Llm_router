from dataclasses import dataclass
from typing import Literal

@dataclass
class Signal:
    tokens : int
    reasoning : bool
    latency : Literal["low", "medium", "high"]
    multimodal : bool
    safety_score : float

def extract_signal(query: str, multimodal: bool) -> Signal:
    """let's write a function to generate the signal for a prompt"""
    words = query.split()

    tokens = int(len(words) * 1.5)

    reasoning_keywords = [
        "reasoning", "step-by-step", "explain", "analyze", "think", "solve",
        "understand", "derive", "derivation", "theory", "complex", "detail",
        "logic", "proof", "prove", "calculate", "math", "code", "programming",
        "algorithm", "why", "how", "compare", "contrast", "evaluate"
    ]
    reasoning = any(keyword in query.lower() for keyword in reasoning_keywords)

    latency = "medium"

    low_latency_keywords = ["quickly", "fast", "short", "brief", "summary", "summarize", "tl;dr", "instant"]
    high_latency_keywords = ["detailed", "comprehensive", "deep dive", "thorough", "extensive", "long"]

    if any(k in query.lower() for k in low_latency_keywords):
        latency = "low"
    elif any(k in query.lower() for k in high_latency_keywords):
        latency = "high"

    unsafe_keywords = [
        "hack", "kill", "steal", "bomb", "murder", "suicide", "terror", 
        "poison", "drug", "weapon", "attack", "exploit", "malware"
    ]
    if any(word in query.lower() for word in unsafe_keywords):
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
