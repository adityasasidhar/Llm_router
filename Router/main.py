import asyncio
import dspy
from Signals import extract_signal, Signal
from Hard_Route import hard_route, ModelName
from Policy_Optimization import policy_route, score_models
from task_classification import TaskClassifier
from typing import Literal, Optional, Dict, Any
from concurrent.futures import ThreadPoolExecutor

lm = dspy.LM(
    model="ollama_chat/qwen3:0.6b",
    api_base="http://localhost:11434",
    api_key="",
    num_retries=2,
    temperature=0.3,
)
dspy.configure(lm=lm)

# Thread pool for running sync DSPy calls
_executor = ThreadPoolExecutor(max_workers=4)


class UnifiedRouter:
    """
    Unified LLM Router with multiple routing strategies:
    - hard_route: Rule-based routing using hard-coded logic
    - policy_route: Score-based optimization for best model selection
    """

    def __init__(self):
        self.task_classifier = TaskClassifier()

    async def route(self, query: str, multimodal: bool = False) -> Dict[str, Any]:
        """
        Route a query to the appropriate model.

        Args:
            query: The user's query
            multimodal: Whether the query involves multimodal content (images, etc.)

        Returns:
            Dictionary with routing decision and metadata
        """
        # Extract signal from query (fast, no I/O)
        signal = extract_signal(query, multimodal)
        
        # Run task classification in thread pool (DSPy calls are sync)
        loop = asyncio.get_event_loop()
        try:
            complexity = await loop.run_in_executor(
                _executor, 
                self.task_classifier, 
                query
            )
        except Exception as e:
            print(f"Warning: Task classification failed ({e}), defaulting to 'medium'")
            complexity = "medium"

        # Try Hard Route first (Fast Path)
        model = hard_route(signal)
        routing_method = "hard_route"

        # If Hard Route returns None, use Policy Route
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

    def route_sync(self, query: str, multimodal: bool = False) -> Dict[str, Any]:
        """Synchronous wrapper for route()."""
        return asyncio.run(self.route(query, multimodal))


async def main():
    router = UnifiedRouter()
    
    # Example usage
    queries = [
        "What is the capital of France?",
        "Explain quantum mechanics step-by-step",
        "Describe this image",
    ]
    
    # Route multiple queries concurrently
    tasks = [router.route(q, multimodal=(i == 2)) for i, q in enumerate(queries)]
    results = await asyncio.gather(*tasks)
    
    for query, result in zip(queries, results):
        print(f"Query: {query}")
        print(f"  Model: {result['model']}")
        print(f"  Method: {result['routing_method']}")
        print()


if __name__ == "__main__":
    asyncio.run(main())
