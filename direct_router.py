
import dspy
from typing import Literal

lm = dspy.LM(
    model="ollama_chat/qwen3:0.6b",
    api_base="http://localhost:11434",
    api_key="",
    num_retries=2,
    temperature=0.2,
)
dspy.configure(lm=lm)

class RouteDecision(dspy.Signature):
    query: str = dspy.InputField(
        desc="A user Query"
    )
    model: Literal[
        "qwen3:1.7b",
        "gpt-oss:20b",
        "gemma3:1b",
        "gpt-4o",
        "claude-haiku-3.5"
    ] = dspy.OutputField(
        desc=(
            "Select the smallest model that can reliably handle the task. "
            "Prefer speed and locality unless deep reasoning or long context "
            "is required."
        )
    )

class LlmRouter(dspy.Module):
    def __init__(self):
        super().__init__()
        self.route = dspy.Predict(RouteDecision)

    def forward(self, query: str):
        decision = self.route(query=query)
        return {
            "model": decision.model,
        }

if __name__ == "__main__":
    router = LlmRouter()
    out = router(query="Write a short poem about the sea.")
    print(out)
