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
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#6366f1', 'primaryTextColor': '#fff', 'primaryBorderColor': '#4f46e5', 'lineColor': '#a78bfa', 'secondaryColor': '#f0abfc', 'tertiaryColor': '#fef3c7', 'edgeLabelBackground':'#fff'}}}%%
flowchart TD
    subgraph Input["📥 INPUT LAYER"]
        A[/"🗣️ User Query"/]
        M{{"🖼️ Multimodal?"}}
    end

    subgraph Signal["🔍 SIGNAL EXTRACTION"]
        B["📊 Token Counter"]
        C["🧠 Reasoning Detector"]
        D["⚡ Latency Analyzer"]
        E["🛡️ Safety Scorer"]
    end

    subgraph Classification["🏷️ TASK CLASSIFICATION"]
        F[["DSPy Classifier"]]
        G["Low Complexity"]
        H["Medium Complexity"]  
        I["High Complexity"]
    end

    subgraph Routing["🚦 ROUTING ENGINE"]
        J{{"Tier 1: Hard Route"}}
        K{{"Tier 2: Policy Route"}}
        L["Score All Models"]
        N["Select Highest Score"]
    end

    subgraph Models["🤖 MODEL POOL"]
        O["gemma3:1b<br/>Simple & Fast"]
        P["qwen3:0.6b-8b<br/>Reasoning"]
        Q["ministral-3:3b-14b<br/>Multimodal"]
        R["gpt-oss:20b<br/>All Capabilities"]
    end

    subgraph Output["📤 OUTPUT"]
        S[/"✅ Selected Model"/]
        T["📋 Routing Metadata"]
    end

    A --> M
    M --> B & C & D & E
    
    B & C & D & E --> F
    
    F --> G & H & I
    
    G & H & I --> J
    
    J -->|"Match Found ✓"| S
    J -->|"No Match"| K
    
    K --> L
    L --> N
    N --> O & P & Q & R
    O & P & Q & R --> S
    S --> T

    style Input fill:#1e1b4b,stroke:#6366f1,color:#e0e7ff
    style Signal fill:#312e81,stroke:#818cf8,color:#e0e7ff
    style Classification fill:#4c1d95,stroke:#a78bfa,color:#f5f3ff
    style Routing fill:#581c87,stroke:#c084fc,color:#faf5ff
    style Models fill:#701a75,stroke:#e879f9,color:#fdf4ff
    style Output fill:#14532d,stroke:#4ade80,color:#dcfce7
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

```
┌─────────────────────────────────────────────────────────────────┐
│  LOW          │  MEDIUM              │  HIGH                    │
│  ─────        │  ────────            │  ────                    │
│  • Greetings  │  • Multi-step tasks  │  • Complex reasoning     │
│  • Simple Q&A │  • Context-dependent │  • Long-form generation  │
│  • Basic cmds │  • Moderate analysis │  • Technical problems    │
└─────────────────────────────────────────────────────────────────┘
```

### Step 3: Two-Tier Routing

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#0ea5e9', 'lineColor': '#38bdf8'}}}%%
graph LR
    subgraph T1["⚡ TIER 1: Hard Route"]
        A["Rule-Based Engine"]
        B["Immediate Decisions"]
        C["Zero Latency"]
    end
    
    subgraph T2["🎯 TIER 2: Policy Route"]
        D["Score Calculator"]
        E["Optimization"]
        F["Best Fit Selection"]
    end
    
    T1 -->|Fallback| T2
    
    style T1 fill:#0c4a6e,stroke:#0ea5e9,color:#e0f2fe
    style T2 fill:#1e3a5f,stroke:#38bdf8,color:#e0f2fe
```

#### Tier 1: Hard Route (Fast Path)
Handles obvious cases with zero computation:
- 🚫 **Unsafe Content** → Blocked immediately
- 💬 **Simple Tasks** → `gemma3:1b`
- 🧠 **Reasoning Tasks** → `qwen` family
- 🖼️ **Multimodal Tasks** → `ministral` or `gpt-oss:20b`

#### Tier 2: Policy Route (Optimization Path)
Calculates weighted compatibility scores:

```
┌──────────────────────────────────────────────────────────────┐
│                    SCORING WEIGHTS                           │
├──────────────────┬───────────────────────────────────────────┤
│ Capability Match │ ████████████████████████░░░░░░░░░░░░ 40%  │
│ Complexity Match │ ██████████████████░░░░░░░░░░░░░░░░░░ 30%  │
│ Latency Match    │ ████████████░░░░░░░░░░░░░░░░░░░░░░░░ 20%  │
│ Token Handling   │ ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 10%  │
└──────────────────┴───────────────────────────────────────────┘
```

---

## 🤖 Supported Models

```mermaid
%%{init: {'theme': 'base'}}%%
graph TB
    subgraph Small["🐇 Small & Fast (< 4B)"]
        A["qwen3:0.6b<br/>🧠 Reasoning"]
        B["gemma3:1b<br/>💬 Instructions"]
        C["ministral-3:3b<br/>🖼️ Multimodal"]
    end
    
    subgraph Medium["🦊 Medium (4B-8B)"]
        D["qwen3:4b<br/>🧠 Reasoning"]
        E["ministral-3:8b<br/>🖼️ Multimodal"]
        F["qwen3:8b<br/>🧠 Reasoning"]
    end
    
    subgraph Large["🦁 Large (> 8B)"]
        G["ministral-3:14b<br/>🖼️ Multimodal"]
        H["gpt-oss:20b<br/>🧠🖼️ Everything"]
    end
    
    style Small fill:#dbeafe,stroke:#3b82f6,color:#1e3a8a
    style Medium fill:#fef3c7,stroke:#f59e0b,color:#78350f
    style Large fill:#fee2e2,stroke:#ef4444,color:#7f1d1d
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
