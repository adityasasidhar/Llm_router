import dspy
from Signals import extract_signal, Signal
from Hard_Route import hard_route, ModelName
from Policy_Optimization import policy_route, score_models
from task_classification import TaskClassifier
from typing import Literal, Optional, Dict, Any

lm = dspy.LM(
    model="ollama_chat/qwen3:0.6b",
    api_base="http://localhost:11434",
    api_key="",
    num_retries=2,
    temperature=0.3,
)
dspy.configure(lm=lm)


class UnifiedRouter:
    """
    Unified LLM Router with multiple routing strategies:
    - hard_route: Rule-based routing using hard-coded logic
    - policy_route: Score-based optimization for best model selection
    - cot_route: Chain-of-thought reasoning for routing decisions
    """

    def __init__(self):
        self.task_classifier = TaskClassifier()

    def route(self, query: str, multimodal: bool = False) -> Dict[str, Any]:
        """
        Route a query to the appropriate model.

        Args:
            query: The user's query
            multimodal: Whether the query involves multimodal content (images, etc.)

        Returns:
            Dictionary with routing decision and metadata
        """
        # Extract signal from query
        signal = extract_signal(query, multimodal)
        
        # Determine complexity
        try:
            complexity = self.task_classifier(query)
        except Exception as e:
            print(f"Warning: Task classification failed ({e}), defaulting to 'medium'")
            complexity = "medium"

        # Try Hard Route first (Fast Path)
        model = hard_route(signal)
        routing_method = "hard_route"

        # If Hard Route returns None or we want to optimize, use Policy Route
        if model is None:
            model = policy_route(signal, complexity)
            routing_method = "policy_route"

        return {
            "model": model,
            "routing_method": routing_method,
            "complexity": complexity,
            "signal": {
                "tokens": signal.tokens,
                "reasoning": signal.reasoning,
                "latency": signal.latency,
                "multimodal": signal.multimodal,
                "safety_score": signal.safety_score,
            }
        }

def main():
    router = UnifiedRouter()
    
    # Example usage
    query = "Explain quantum mechanics step-by-step"
    result = router.route(query)
    print(f"Query: {query}")
    print(f"Selected Model: {result['model']}")
    print(f"Method: {result['routing_method']}")

if __name__ == "__main__":
    main()
