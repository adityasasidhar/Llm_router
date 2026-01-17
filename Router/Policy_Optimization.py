from task_classification import *
from Hard_Route import ModelName
from Signals import Signal
from typing import Dict, List, Tuple, Optional

# Model capabilities and characteristics
MODEL_SPECS = {
    "gemma3:1b": {"size": 1, "reasoning": False, "multimodal": False, "speed": 10},
    "qwen3:0.6b": {"size": 0.6, "reasoning": True, "multimodal": False, "speed": 12},
    "ministral-3:3b": {"size": 3, "reasoning": False, "multimodal": True, "speed": 8},
    "qwen3:4b": {"size": 4, "reasoning": True, "multimodal": False, "speed": 6},
    "ministral-3:8b": {"size": 8, "reasoning": False, "multimodal": True, "speed": 4},
    "qwen3:8b": {"size": 8, "reasoning": True, "multimodal": False, "speed": 4},
    "ministral-3:14b": {"size": 14, "reasoning": False, "multimodal": True, "speed": 2},
    "gpt-oss:20b": {"size": 20, "reasoning": True, "multimodal": True, "speed": 1},
}

def score_models(model: ModelName, complexity: str, signal: Signal) -> float:
    """
    Score a model based on how well it matches the task requirements.
    Returns a score from 0.0 to 1.0, where higher is better.
    """
    if model not in MODEL_SPECS:
        return 0.0

    spec = MODEL_SPECS[model]
    score = 0.0

    # Capability matching (40% of score)
    capability_score = 0.0

    # Check if model can handle reasoning requirement
    if signal.reasoning:
        if spec["reasoning"]:
            capability_score += 0.5
        else:
            return 0.0  # Cannot handle this task
    else:
        capability_score += 0.5

    # Check if model can handle multimodal requirement
    if signal.multimodal:
        if spec["multimodal"]:
            capability_score += 0.5
        else:
            return 0.0  # Cannot handle this task
    else:
        capability_score += 0.5

    score += capability_score * 0.4

    # Complexity matching (30% of score)
    complexity_score = 0.0
    if complexity == "low":
        # Prefer smaller models for low complexity
        complexity_score = 1.0 - (spec["size"] / 20)
    elif complexity == "medium":
        # Prefer mid-sized models
        if 3 <= spec["size"] <= 8:
            complexity_score = 1.0
        else:
            complexity_score = 0.6
    else:  # high complexity
        # Prefer larger models
        complexity_score = spec["size"] / 20

    score += complexity_score * 0.3

    # Latency matching (20% of score)
    latency_score = 0.0
    if signal.latency == "low":
        # Prefer faster models
        latency_score = spec["speed"] / 12
    elif signal.latency == "medium":
        latency_score = 0.8
    else:  # high latency tolerance
        latency_score = 1.0

    score += latency_score * 0.2

    # Token handling (10% of score)
    token_score = 0.0
    if signal.tokens < 1000:
        # Small models can handle this
        token_score = 1.0
    elif signal.tokens < 3000:
        # Need medium to large model
        if spec["size"] >= 3:
            token_score = 1.0
        else:
            token_score = 0.5
    else:
        # Need large model
        if spec["size"] >= 8:
            token_score = 1.0
        else:
            token_score = 0.3

    score += token_score * 0.1

    return score


def policy_route(signal: Signal, complexity: str) -> Optional[ModelName]:
    """
    Route based on policy optimization - score all models and select the best one.
    """
    if signal.safety_score < 0.5:
        return None

    all_models: List[ModelName] = [
        "gemma3:1b", "qwen3:0.6b", "ministral-3:3b", "qwen3:4b",
        "ministral-3:8b", "qwen3:8b", "ministral-3:14b", "gpt-oss:20b"
    ]

    scores: List[Tuple[ModelName, float]] = []
    for model in all_models:
        score = score_models(model, complexity, signal)
        if score > 0:
            scores.append((model, score))

    # Sort by score (descending) and return the best model
    scores.sort(key=lambda x: x[1], reverse=True)

    if scores:
        return scores[0][0]

    return "gpt-oss:20b"  # Fallback to most capable model

