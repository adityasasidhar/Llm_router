from typing import Literal
import dspy

class TaskClass(dspy.Signature):
    query: str = dspy.InputField()
    complexity: Literal["low", "medium", "high"] = dspy.OutputField()

class TaskClassifier(dspy.Module):
    def __init__(self):
        super().__init__()
        self.classify = dspy.Predict(TaskClass)

    def forward(self, query: str) -> Literal["low", "medium", "high"]:
        result = self.classify(query=query)
        return result.complexity


