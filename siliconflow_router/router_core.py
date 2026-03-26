"""
Shared routing logic for SiliconFlow vs Moonshot (official Kimi API) profiles.
OpenClaw model refs: siliconflow/<api_model_id> | moonshot/<api_model_id>
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional

Profile = Literal["siliconflow", "moonshot"]

VALID_PROFILES: tuple[str, ...] = ("siliconflow", "moonshot")

# --- SiliconFlow: hosted third-party IDs (SiliconFlow API) ---
SILICONFLOW_REGISTRY: Dict[str, Dict[str, Any]] = {
    "qwen3-235b": {
        "id": "Qwen/Qwen3-235B-A22B",
        "tier": 1,
        "capabilities": ["reasoning", "complex", "long-context"],
        "cost_input": 0.003,
        "cost_output": 0.006,
        "context": 128000,
    },
    "deepseek-r1": {
        "id": "deepseek-ai/DeepSeek-R1",
        "tier": 1,
        "capabilities": ["math", "coding", "reasoning"],
        "cost_input": 0.002,
        "cost_output": 0.008,
        "context": 64000,
    },
    "kimi-k2-thinking": {
        "id": "moonshotai/Kimi-K2-Thinking",
        "tier": 1,
        "capabilities": ["long-context", "reasoning"],
        "cost_input": 0.002,
        "cost_output": 0.006,
        "context": 256000,
    },
    "glm-4.5": {
        "id": "zai-org/GLM-4.5",
        "tier": 1,
        "capabilities": ["chinese", "complex"],
        "cost_input": 0.002,
        "cost_output": 0.004,
        "context": 128000,
    },
    "qwen3-coder-480b": {
        "id": "Qwen/Qwen3-Coder-480B-A35B-Instruct",
        "tier": 2,
        "capabilities": ["coding", "architecture"],
        "cost_input": 0.002,
        "cost_output": 0.005,
        "context": 128000,
    },
    "kimi-dev-72b": {
        "id": "moonshotai/Kimi-Dev-72B",
        "tier": 2,
        "capabilities": ["coding", "debugging"],
        "cost_input": 0.001,
        "cost_output": 0.003,
        "context": 128000,
    },
    "qwen2.5-coder-32b": {
        "id": "Qwen/Qwen2.5-Coder-32B-Instruct",
        "tier": 2,
        "capabilities": ["coding", "fast"],
        "cost_input": 0.0008,
        "cost_output": 0.0015,
        "context": 128000,
    },
    "qwen3-vl-235b": {
        "id": "Qwen/Qwen3-VL-235B-A22B-Thinking",
        "tier": 3,
        "capabilities": ["vision", "reasoning", "complex"],
        "cost_input": 0.004,
        "cost_output": 0.008,
        "context": 128000,
    },
    "glm-4.6v": {
        "id": "zai-org/GLM-4.6V",
        "tier": 3,
        "capabilities": ["vision", "high-res"],
        "cost_input": 0.002,
        "cost_output": 0.004,
        "context": 32000,
    },
    "qwen2.5-vl-72b": {
        "id": "Qwen/Qwen2.5-VL-72B-Instruct",
        "tier": 3,
        "capabilities": ["vision", "general"],
        "cost_input": 0.001,
        "cost_output": 0.002,
        "context": 32000,
    },
    "qwen3-32b": {
        "id": "Qwen/Qwen3-32B",
        "tier": 4,
        "capabilities": ["general", "fast", "balanced"],
        "cost_input": 0.0005,
        "cost_output": 0.001,
        "context": 128000,
    },
    "deepseek-v3": {
        "id": "deepseek-ai/DeepSeek-V3",
        "tier": 4,
        "capabilities": ["general", "coding"],
        "cost_input": 0.0004,
        "cost_output": 0.001,
        "context": 64000,
    },
    "qwen3-8b": {
        "id": "Qwen/Qwen3-8B",
        "tier": 5,
        "capabilities": ["fast", "simple"],
        "cost_input": 0.0001,
        "cost_output": 0.0002,
        "context": 32000,
    },
    "qwen2.5-7b": {
        "id": "Qwen/Qwen2.5-7B-Instruct",
        "tier": 5,
        "capabilities": ["fast", "simple", "chat"],
        "cost_input": 0.00005,
        "cost_output": 0.0001,
        "context": 32000,
    },
}

# --- Moonshot Open Platform: official model IDs only (same as moonshot/<id> in OpenClaw) ---
MOONSHOT_REGISTRY: Dict[str, Dict[str, Any]] = {
    "kimi-k2-thinking": {
        "id": "kimi-k2-thinking",
        "tier": 1,
        "capabilities": ["reasoning", "long-context", "coding"],
        "cost_input": 0.0,
        "cost_output": 0.0,
        "context": 256000,
    },
    "kimi-k2-thinking-turbo": {
        "id": "kimi-k2-thinking-turbo",
        "tier": 2,
        "capabilities": ["reasoning", "fast"],
        "cost_input": 0.0,
        "cost_output": 0.0,
        "context": 256000,
    },
    "kimi-k2.5": {
        "id": "kimi-k2.5",
        "tier": 3,
        "capabilities": ["general", "balanced", "coding"],
        "cost_input": 0.0,
        "cost_output": 0.0,
        "context": 256000,
    },
    "kimi-k2-0905-preview": {
        "id": "kimi-k2-0905-preview",
        "tier": 4,
        "capabilities": ["general", "fast"],
        "cost_input": 0.0,
        "cost_output": 0.0,
        "context": 256000,
    },
    "kimi-k2-turbo-preview": {
        "id": "kimi-k2-turbo-preview",
        "tier": 5,
        "capabilities": ["fast", "simple"],
        "cost_input": 0.0,
        "cost_output": 0.0,
        "context": 256000,
    },
}

REGISTRIES: Dict[str, Dict[str, Dict[str, Any]]] = {
    "siliconflow": SILICONFLOW_REGISTRY,
    "moonshot": MOONSHOT_REGISTRY,
}

TIER_NAMES: Dict[int, str] = {
    1: "旗舰推理",
    2: "专业代码 / 推理加速",
    3: "视觉 / 旗舰通用",
    4: "平衡通用",
    5: "极速经济",
}

TIER_NAMES_MOONSHOT: Dict[int, str] = {
    1: "深度推理 (Thinking)",
    2: "推理加速 (Thinking Turbo)",
    3: "旗舰通用 (K2.5)",
    4: "预览版 (0905)",
    5: "极速 (Turbo)",
}

MODE_MAP_SILICONFLOW: Dict[str, str] = {
    "power": "qwen3-235b",
    "fast": "qwen3-8b",
    "code": "qwen3-coder-480b",
    "vision": "qwen3-vl-235b",
}

MODE_MAP_MOONSHOT: Dict[str, str] = {
    "power": "kimi-k2-thinking",
    "fast": "kimi-k2-turbo-preview",
    "code": "kimi-k2-thinking",
    "vision": "kimi-k2-thinking",
}


def normalize_profile(name: Optional[str]) -> Profile:
    if name == "moonshot":
        return "moonshot"
    return "siliconflow"


def get_registry(profile: Profile) -> Dict[str, Dict[str, Any]]:
    return REGISTRIES[profile]


def openclaw_model_ref(profile: Profile, model_info: Dict[str, Any]) -> str:
    mid = model_info["id"]
    if profile == "moonshot":
        return f"moonshot/{mid}"
    return f"siliconflow/{mid}"


def analyze_intent(query: str, has_image: bool = False) -> Dict[str, Any]:
    if has_image:
        return {
            "type": "vision",
            "complexity": "high"
            if any(k in query for k in ["分析", "解释", "图表", "推理"])
            else "normal",
            "reason": "图像输入",
        }
    orchestration_kw = [
        "多任务",
        "多步骤",
        "分阶段",
        "端到端",
        "全链路",
        "流水线",
        "拆解任务",
        "并行",
        "multi-task",
        "multitask",
        "multi step",
        "workflow",
        "pipeline",
        "orchestration",
    ]
    if any(k in query.lower() for k in orchestration_kw):
        return {"type": "reasoning", "complexity": "high", "reason": "多任务/编排类任务"}
    code_kw = [
        "代码",
        "编程",
        "函数",
        "类",
        "bug",
        "debug",
        "架构",
        "设计模式",
        "重构",
        "算法",
        "code",
        "function",
        "class",
        "implement",
        "refactor",
    ]
    if any(k in query.lower() for k in code_kw):
        complexity = (
            "high"
            if any(k in query for k in ["架构", "重构", "设计模式", "系统", "复杂"])
            else "normal"
        )
        return {"type": "coding", "complexity": complexity, "reason": "代码相关任务"}
    reasoning_kw = [
        "为什么",
        "分析",
        "推导",
        "证明",
        "逻辑",
        "推理",
        "数学",
        "计算",
        "why",
        "analyze",
        "prove",
        "reason",
    ]
    if any(k in query.lower() for k in reasoning_kw):
        return {"type": "reasoning", "complexity": "high", "reason": "复杂推理任务"}
    long_context_kw = [
        "长任务",
        "长文本",
        "超长",
        "上下文很长",
        "万字",
        "长文档",
        "全量日志",
        "全部代码",
        "long context",
        "long-context",
        "large context",
        "huge prompt",
    ]
    if len(query) > 8000 or any(k in query.lower() for k in long_context_kw):
        return {"type": "long-context", "complexity": "high", "reason": "长上下文任务"}
    return {"type": "general", "complexity": "normal", "reason": "一般对话"}


@dataclass
class RouterState:
    mode: str = "auto"
    forced_model: Optional[str] = None
    usage_stats: Dict[str, Any] = field(
        default_factory=lambda: {
            "total_requests": 0,
            "total_cost": 0.0,
            "model_distribution": {},
        }
    )


def _pick_siliconflow(intent: Dict[str, Any], priority: str) -> List[str]:
    t, c = intent["type"], intent["complexity"]
    if t == "vision":
        # Vision tasks are the slowest path; we need a reliable "fast enough" model first.
        # Runtime evidence shows `qwen2.5-vl-72b` can fail with provider HTTP 400, so we avoid it by default.
        # For normal extraction-like queries: prefer `glm-4.6v`, then fall back to `qwen3-vl-235b`.
        # For complex vision: keep `qwen3-vl-235b` first, then `glm-4.6v`.
        return ["qwen3-vl-235b", "glm-4.6v"] if c == "high" else ["glm-4.6v", "qwen3-vl-235b"]
    if t == "coding":
        return ["qwen3-coder-480b", "kimi-dev-72b"] if c == "high" else ["qwen2.5-coder-32b", "deepseek-v3"]
    if t == "reasoning":
        return ["deepseek-r1", "qwen3-235b", "kimi-k2-thinking"]
    if t == "long-context":
        return ["kimi-k2-thinking", "qwen3-235b"]
    if priority == "quality":
        return ["qwen3-32b", "deepseek-v3", "glm-4.5"]
    return ["qwen3-8b", "qwen2.5-7b"]


def _pick_moonshot(intent: Dict[str, Any], priority: str) -> List[str]:
    """Only official Moonshot / Kimi Open Platform model IDs."""
    t, c = intent["type"], intent["complexity"]
    if t == "vision":
        # K2 列表以文本为主；图像场景用最强推理模型兜底（多模态以控制台实际能力为准）
        return ["kimi-k2-thinking", "kimi-k2-thinking-turbo"]
    if t == "coding":
        return (
            ["kimi-k2-thinking", "kimi-k2-thinking-turbo"]
            if c == "high"
            else ["kimi-k2.5", "kimi-k2-0905-preview"]
        )
    if t in ("reasoning", "long-context"):
        return ["kimi-k2-thinking", "kimi-k2-thinking-turbo", "kimi-k2.5"]
    if priority == "quality":
        return ["kimi-k2.5", "kimi-k2-0905-preview", "kimi-k2-thinking"]
    return ["kimi-k2-turbo-preview", "kimi-k2-0905-preview"]


def select_model_key(
    intent: Dict[str, Any],
    priority: str,
    profile: Profile,
    state: RouterState,
) -> tuple[str, Dict[str, Any], str]:
    registry = get_registry(profile)
    mode_map = MODE_MAP_MOONSHOT if profile == "moonshot" else MODE_MAP_SILICONFLOW

    if state.mode != "auto" and state.forced_model and state.forced_model in registry:
        key = state.forced_model
        return key, registry[key], f"强制模式: {state.mode}, model_key={key}"

    if state.mode in mode_map:
        key = mode_map[state.mode]
        return key, registry[key], f"手动模式: {state.mode}"

    candidates = _pick_moonshot(intent, priority) if profile == "moonshot" else _pick_siliconflow(intent, priority)
    for key in candidates:
        if key in registry:
            reason = f"意图识别: {intent['type']}({intent['complexity']}), 策略: {priority}"
            return key, registry[key], reason

    default_key = "kimi-k2.5" if profile == "moonshot" else "qwen3-32b"
    return default_key, registry[default_key], "回退默认模型"


def estimate_cost(
    profile: Profile,
    model_key: str,
    input_tokens: int = 1000,
    output_tokens: int = 500,
) -> Dict[str, Any]:
    registry = get_registry(profile)
    model = registry[model_key]
    inp = (input_tokens / 1000) * model["cost_input"]
    out = (output_tokens / 1000) * model["cost_output"]
    total = inp + out
    out: Dict[str, Any] = {
        "input_cost": round(inp, 6),
        "output_cost": round(out, 6),
        "total": round(total, 6),
        "currency": "CNY",
    }
    if profile == "moonshot":
        out["note"] = "Moonshot 单价以控制台为准；可在 router_core.py 中补 cost_input/cost_output"
    return out


def fallback_keys(profile: Profile, model_key: str, limit: int = 3) -> List[str]:
    registry = get_registry(profile)
    info = registry.get(model_key)
    if not info:
        return []
    tier = info["tier"]
    keys = [
        k
        for k, v in registry.items()
        if tier <= v["tier"] <= min(tier + 1, 5)
    ]
    return keys[:limit]
