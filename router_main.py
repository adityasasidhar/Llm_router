import dspy
from typing import Literal

lm = dspy.LM(
    model="ollama_chat/qwen3:0.6b",
    api_base="http://localhost:11434",
    api_key="",
    num_retries=2,
    temperature=0.7,
)

dspy.configure(lm=lm)

class Response(dspy.Signature):
    query: str = dspy.InputField(desc="The query")
    models: Literal[
        "qwen3:1.7b",
        "ibm/granite4:3b",
        "gpt-oss:20b"
    ] = dspy.OutputField(desc="The model to select")


class COT(dspy.Signature):
    query: str = dspy.InputField(desc="The task or query")
    cot_answer: str = dspy.OutputField(desc="Reasoning about the task")


class LlmRouter(dspy.Module):
    def __init__(self):
        super().__init__()
        self.think = dspy.ChainOfThought(COT)
        self.route = dspy.Predict(Response)

    def forward(self, query: str):
        thought = self.think(query=query)
        decision = self.route(query=query)
        return {
            "cot_answer": thought.cot_answer,
            "models": decision.models,
        }

router = LlmRouter()
out = router(query="I need fast local reasoning for coding tasks")
print(out)
