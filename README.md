# 🤖 LLM Router

> **Intelligent query routing for optimal model selection** — A sophisticated, multi-strategy LLM router designed to intelligently direct user queries to the most appropriate model based on task complexity, required capabilities, and performance constraints.

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)](https://python.org)
[![DSPy](https://img.shields.io/badge/DSPy-Powered-purple)](https://github.com/stanfordnlp/dspy)
[![Ollama](https://img.shields.io/badge/Ollama-Compatible-brightgreen)](https://ollama.com)

---

## 🎯 Overview

LLM Router uses a **unified approach** to select the best model for any given query. It combines rule-based heuristics with score-based optimization to balance **accuracy**, **latency**, and **cost**.

---

## 🔄 Architecture Flow

```mermaid
flowchart TD
    A["🗣️ User Query"] --> M{"🖼️ Multimodal?"}
    
    M --> B["📊 Token Counter"]
    M --> C["🧠 Reasoning Detector"]
    M --> D["⚡ Latency Analyzer"]
    M --> E["🛡️ Safety Scorer"]
    
    B --> F[["DSPy Classifier"]]
    C --> F
    D --> F
    E --> F
    
    F --> G["Low Complexity"]
    F --> H["Medium Complexity"]
    F --> I["High Complexity"]
    
    G --> J{"Tier 1: Hard Route"}
    H --> J
    I --> J
    
    J -->|"Match Found ✓"| S["✅ Selected Model"]
    J -->|"No Match"| K{"Tier 2: Policy Route"}
    
    K --> L["Score All Models"]
    L --> N["Select Highest Score"]
    
    N --> O["gemma3:1b"]
    N --> P["qwen3 family"]
    N --> Q["ministral-3 family"]
    N --> R["gpt-oss:20b"]
    
    O --> S
    P --> S
    Q --> S
    R --> S
    
    S --> T["📋 Routing Metadata"]
```

---

## 🔬 How It Works

### Step 1: Signal Extraction
Every incoming query is analyzed to extract a **Signal** object containing:

| Signal Property | Description | Detection Method |
|----------------|-------------|------------------|
| 📊 **Token Count** | Estimated input length | Word count × 1.5 |
| 🧠 **Reasoning** | Logical/analytical need | Keyword matching |
| ⚡ **Latency** | Response urgency | Context keywords |
| 🖼️ **Multimodal** | Non-text content | Explicit flag |
| 🛡️ **Safety Score** | Content safety (0-1) | Blocklist check |

### Step 2: Task Classification
Using **DSPy**, the router classifies complexity:

| Level | Examples |
|-------|----------|
| **Low** | Greetings, Simple Q&A, Basic commands |
| **Medium** | Multi-step tasks, Context-dependent queries |
| **High** | Complex reasoning, Long-form generation, Technical problems |

### Step 3: Two-Tier Routing

```mermaid
flowchart LR
    A["⚡ Rule-Based Engine"] --> B["Immediate Decisions"]
    B --> C["Zero Latency"]
    C -->|"Fallback"| D["🎯 Score Calculator"]
    D --> E["Optimization"]
    E --> F["Best Fit Selection"]
```

#### Tier 1: Hard Route (Fast Path)
Handles obvious cases with zero computation:
- 🚫 **Unsafe Content** → Blocked immediately
- 💬 **Simple Tasks** → `gemma3:1b`
- 🧠 **Reasoning Tasks** → `qwen` family
- 🖼️ **Multimodal Tasks** → `ministral` or `gpt-oss:20b`

#### Tier 2: Policy Route (Optimization Path)
Calculates weighted compatibility scores:

| Weight | Category |
|--------|----------|
| **40%** | Capability Matching |
| **30%** | Complexity Matching |
| **20%** | Latency Matching |
| **10%** | Token Handling |

---

## 🤖 Supported Models

```mermaid
flowchart LR
    A["qwen3:0.6b 🧠"] --- B["gemma3:1b 💬"]
    B --- C["ministral-3:3b 🖼️"]
    C --- D["qwen3:4b 🧠"]
    D --- E["ministral-3:8b 🖼️"]
    E --- F["qwen3:8b �"]
    F --- G["ministral-3:14b 🖼️"]
    G --- H["gpt-oss:20b 🧠🖼️"]
```

| Model | Size | Reasoning | Multimodal | Speed | Best For |
|:------|:----:|:---------:|:----------:|:-----:|:---------|
| `qwen3:0.6b` | 0.6B | ✅ | ❌ | ⚡⚡⚡ | Tiny reasoning tasks |
| `gemma3:1b` | 1B | ❌ | ❌ | ⚡⚡⚡ | Simple instructions |
| `ministral-3:3b` | 3B | ❌ | ✅ | ⚡⚡ | General multimodal |
| `qwen3:4b` | 4B | ✅ | ❌ | ⚡⚡ | Balanced reasoning |
| `ministral-3:8b` | 8B | ❌ | ✅ | ⚡ | Advanced multimodal |
| `qwen3:8b` | 8B | ✅ | ❌ | ⚡ | Complex reasoning |
| `ministral-3:14b` | 14B | ❌ | ✅ | 🐢 | High-quality multimodal |
| `gpt-oss:20b` | 20B | ✅ | ✅ | 🐢 | Any complex task |

---

## 📁 Project Structure

```
LLmRouter/
├── Router/
│   ├── main.py              # 🚀 UnifiedRouter entry point
│   ├── Signals.py           # 📊 Signal extraction logic
│   ├── task_classification.py # 🏷️ DSPy complexity classifier
│   ├── Hard_Route.py        # ⚡ Rule-based fast routing
│   ├── Policy_Optimization.py # 🎯 Score-based model selection
│   └── test.py              # 🧪 Comprehensive test suite
├── README.md
└── pyproject.toml
```

---

## 🚀 Quick Start

```python
from Router.main import UnifiedRouter

router = UnifiedRouter()

# 💬 Route a simple text query
result = router.route("What is the capital of France?")
print(f"Selected Model: {result['model']}")
# Output: Selected Model: gemma3:1b

# 🧠 Route a reasoning task
result = router.route("Explain quantum mechanics step-by-step")
print(f"Selected Model: {result['model']}")
# Output: Selected Model: qwen3:8b

# 🖼️ Route a multimodal reasoning task
result = router.route("Explain the math in this image", multimodal=True)
print(f"Selected Model: {result['model']}")
# Output: Selected Model: gpt-oss:20b
```

### Response Structure

```python
{
    "model": "qwen3:8b",           # Selected model
    "routing_method": "hard_route", # Which tier was used
    "complexity": "high",           # Classified complexity
    "signal": {
        "tokens": 15,
        "reasoning": True,
        "latency": "medium",
        "multimodal": False,
        "safety_score": 0.95
    }
}
```

---

## 📜 License

MIT License — feel free to use, modify, and distribute.

---

<div align="center">

**Built with ❤️ using [DSPy](https://github.com/stanfordnlp/dspy) and [Ollama](https://ollama.com)**

</div>
