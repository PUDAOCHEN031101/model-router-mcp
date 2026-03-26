#!/usr/bin/env python3
"""
智能路由 MCP Server：支持 siliconflow（硅基流动）与 moonshot（Moonshot 官方 Kimi API）。
环境变量 ROUTER_PROFILE=siliconflow|moonshot 设置默认 profile。
"""

import asyncio
import json
import os
from typing import Any, Optional

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from router_core import (
    Profile,
    RouterState,
    analyze_intent,
    estimate_cost,
    fallback_keys,
    get_registry,
    normalize_profile,
    openclaw_model_ref,
    select_model_key,
)

server = Server("siliconflow-router")


class ModelRouter:
    def __init__(self) -> None:
        self.state = RouterState()
        self.profile: Profile = normalize_profile(os.environ.get("ROUTER_PROFILE", "siliconflow"))


_router = ModelRouter()


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    return [
        Tool(
            name="route_task",
            description="智能路由：分析任务并推荐模型（siliconflow 或 moonshot 官方 Kimi）",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "用户输入内容"},
                    "has_image": {"type": "boolean", "description": "是否包含图像", "default": False},
                    "priority": {
                        "type": "string",
                        "enum": ["quality", "speed", "balanced"],
                        "default": "quality",
                    },
                    "profile": {
                        "type": "string",
                        "enum": ["siliconflow", "moonshot"],
                        "description": "siliconflow=硅基流动；moonshot=仅 Moonshot 开放平台模型",
                    },
                    "estimated_input_tokens": {"type": "integer", "default": 1000},
                    "estimated_output_tokens": {"type": "integer", "default": 500},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="set_mode",
            description="设置路由模式: auto=自动, power=旗舰, fast=极速, code=代码, vision=视觉",
            inputSchema={
                "type": "object",
                "properties": {
                    "mode": {
                        "type": "string",
                        "enum": ["auto", "power", "fast", "code", "vision"],
                    },
                    "specific_model": {"type": "string", "description": "registry 中的 model_key（可选）"},
                    "profile": {
                        "type": "string",
                        "enum": ["siliconflow", "moonshot"],
                        "description": "解释 manual 模式时使用的模型表",
                    },
                },
                "required": ["mode"],
            },
        ),
        Tool(
            name="get_status",
            description="获取当前路由状态、默认 profile 与模式",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="list_models",
            description="列出当前 profile 下可用模型",
            inputSchema={
                "type": "object",
                "properties": {
                    "tier": {"type": "integer", "description": "筛选层级（可选）"},
                    "profile": {
                        "type": "string",
                        "enum": ["siliconflow", "moonshot"],
                    },
                },
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: Optional[dict[str, Any]]) -> list[TextContent]:
    args = arguments or {}

    if name == "route_task":
        query = args.get("query", "")
        has_image = args.get("has_image", False)
        priority = args.get("priority", "quality")
        if priority == "balanced":
            priority = "quality"
        profile: Profile = normalize_profile(args.get("profile") or _router.profile)

        intent = analyze_intent(query, has_image)
        model_key, model_info, sel_reason = select_model_key(intent, priority, profile, _router.state)
        input_tok = args.get("estimated_input_tokens", 1000)
        output_tok = args.get("estimated_output_tokens", 500)
        cost = estimate_cost(profile, model_key, input_tok, output_tok)
        ref = openclaw_model_ref(profile, model_info)
        registry = get_registry(profile)
        fallback_key_chain = fallback_keys(profile, model_key)
        # fallback_chain 对宿主来说更直接：直接给出 openclaw_model_id 兜底候选
        fallback_chain = [
            openclaw_model_ref(profile, registry[k])
            for k in fallback_key_chain
            if k in registry
        ]

        result = {
            "profile": profile,
            "decision": {
                "model_key": model_key,
                "model_id": model_info["id"],
                "tier": model_info["tier"],
                "capabilities": model_info["capabilities"],
                "openclaw_model_id": ref,
                "openclaw_route_tag": f"[[OPENCLAW_ROUTE_MODEL:{ref}]]",
            },
            "routing": {
                "intent_type": intent["type"],
                "intent_complexity": intent["complexity"],
                "reason": sel_reason,
            },
            "cost_estimate": {k: v for k, v in cost.items() if v is not None},
            "fallback_chain": fallback_chain,
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]

    if name == "set_mode":
        mode = args.get("mode", "auto")
        specific = args.get("specific_model")
        prof = normalize_profile(args.get("profile") or _router.profile)
        _router.state.mode = mode
        _router.state.forced_model = specific
        _router.profile = prof
        if prof == "moonshot":
            mode_desc = {
                "auto": "自动路由（Moonshot 官方模型）",
                "power": "旗舰推理 (kimi-k2-thinking)",
                "fast": "极速 (kimi-k2-turbo-preview)",
                "code": "代码/推理 (kimi-k2-thinking)",
                "vision": "视觉意图→推理兜底 (kimi-k2-thinking)",
            }
        else:
            mode_desc = {
                "auto": "自动路由（SiliconFlow）",
                "power": "旗舰模式 (Qwen3-235B)",
                "fast": "极速模式 (Qwen3-8B)",
                "code": "代码专用 (Qwen3-Coder-480B)",
                "vision": "视觉分析 (Qwen3-VL-235B)",
            }
        return [TextContent(type="text", text=f"已切换到 {mode_desc.get(mode, mode)} (profile={prof})")]

    if name == "get_status":
        status = {
            "default_profile": _router.profile,
            "ROUTER_PROFILE_env": os.environ.get("ROUTER_PROFILE", ""),
            "current_mode": _router.state.mode,
            "forced_model": _router.state.forced_model,
            "siliconflow_models": len(get_registry("siliconflow")),
            "moonshot_models": len(get_registry("moonshot")),
        }
        return [TextContent(type="text", text=json.dumps(status, indent=2))]

    if name == "list_models":
        tier_filter = args.get("tier")
        profile = normalize_profile(args.get("profile") or _router.profile)
        registry = get_registry(profile)
        models = {
            k: v
            for k, v in registry.items()
            if tier_filter is None or v["tier"] == tier_filter
        }
        return [TextContent(type="text", text=json.dumps(models, indent=2, ensure_ascii=False))]

    return [TextContent(type="text", text=f"未知工具: {name}")]


async def main() -> None:
    async with stdio_server(server) as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="siliconflow-router",
                server_version="0.2.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
