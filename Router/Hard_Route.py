from Signals import Signal
from typing import Optional, Literal

ModelName = Literal["gemma3:1b", "qwen3:0.6b",
"ministral-3:3b", "qwen3:4b",
"ministral-3:8b", "qwen3:8b",
"ministral-3:14b", "gpt-oss:20b"]


def hard_route(signal: Signal) -> Optional[ModelName]:
    """
    Route to appropriate model based on signal characteristics.

    Model capabilities:
    - qwen models: Reasoning only
    - ministral models: Multimodal + instruct (no reasoning)
    - gemma3:1b: Instruct only
    - gpt-oss:20b: Multimodal + reasoning (can do everything)
    """

    # Handle unsafe content
    if signal.safety_score < 0.5:
        return None

    # 1. Multimodal Handling
    if signal.multimodal:
        if signal.reasoning:
            return "gpt-oss:20b"
        # Simple multimodal -> prefer ministral family
        if signal.latency == "low":
            return "ministral-3:3b"
        return "ministral-3:8b"

    # 2. Reasoning Handling
    if signal.reasoning:
        if signal.latency == "low":
            return "qwen3:4b"  # Good balance
        return "qwen3:8b"  # Better reasoning

    # 3. Standard Text Handling (No reasoning, No image)
    if signal.latency == "low":
        return "gemma3:1b"

    if signal.tokens < 2000:
        return "ministral-3:3b"

    return "ministral-3:8b"
