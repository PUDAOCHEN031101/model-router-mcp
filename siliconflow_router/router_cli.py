#!/usr/bin/env python3
"""
智能模型路由 CLI（SiliconFlow 或 Moonshot 官方 Kimi API）
用法:
  python3 router_cli.py route "帮我写代码"
  python3 router_cli.py route "Kimi 官方" --profile moonshot
  python3 router_cli.py list [--profile moonshot] [--tier 2]
  python3 router_cli.py models [--profile moonshot]
"""

import argparse
import json
import sys

from router_core import (
    TIER_NAMES,
    TIER_NAMES_MOONSHOT,
    RouterState,
    analyze_intent,
    estimate_cost,
    get_registry,
    normalize_profile,
    openclaw_model_ref,
    select_model_key,
)


def json_dump(data: object) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_route(args: argparse.Namespace) -> None:
    query = " ".join(args.query)
    profile = normalize_profile(args.profile)
    state = RouterState()
    intent = analyze_intent(query, args.image)
    model_key, model_info, sel_reason = select_model_key(intent, args.priority, profile, state)
    cost = estimate_cost(profile, model_key, args.input_tokens, args.output_tokens)
    ref = openclaw_model_ref(profile, model_info)
    tier_names = TIER_NAMES_MOONSHOT if profile == "moonshot" else TIER_NAMES
    tier_label = tier_names.get(model_info["tier"], str(model_info["tier"]))
    result = {
        "推荐模型": model_info["id"],
        "model_key": model_key,
        "router_profile": profile,
        "tier": f"Tier-{model_info['tier']} ({tier_label})",
        "capabilities": model_info["capabilities"],
        "意图分析": f"{intent['type']} ({intent['complexity']}) — {intent['reason']}",
        "路由说明": sel_reason,
        "预估成本(CNY)": cost["total"],
        "openclaw_model_id": ref,
        "openclaw_route_tag": f"[[OPENCLAW_ROUTE_MODEL:{ref}]]",
    }
    if "note" in cost:
        result["cost_note"] = cost["note"]
    json_dump(result)


def cmd_list(args: argparse.Namespace) -> None:
    profile = normalize_profile(args.profile)
    registry = get_registry(profile)
    tier_filter = args.tier
    out: dict[str, object] = {}
    for k, v in registry.items():
        if tier_filter is None or v["tier"] == tier_filter:
            out[k] = v
    json_dump(out)


def cmd_models(args: argparse.Namespace) -> None:
    profile = normalize_profile(args.profile)
    registry = get_registry(profile)
    tier_names = TIER_NAMES_MOONSHOT if profile == "moonshot" else TIER_NAMES
    tiers = sorted({v["tier"] for v in registry.values()})
    for tier in tiers:
        print(f"\nTier-{tier} {tier_names.get(tier, '')}:")
        for k, v in registry.items():
            if v["tier"] == tier:
                print(f"  {k:<28} {v['id']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="OpenClaw 智能路由 CLI (siliconflow | moonshot)")
    sub = parser.add_subparsers(dest="cmd")

    p_route = sub.add_parser("route", help="分析查询，推荐模型")
    p_route.add_argument("query", nargs="+")
    p_route.add_argument(
        "--profile",
        default="siliconflow",
        choices=["siliconflow", "moonshot"],
        help="siliconflow=硅基流动托管模型；moonshot=仅 Moonshot 开放平台 Kimi 官方模型 ID",
    )
    p_route.add_argument("--image", action="store_true", help="包含图像")
    p_route.add_argument("--priority", default="quality", choices=["quality", "speed"])
    p_route.add_argument("--input-tokens", type=int, default=1000)
    p_route.add_argument("--output-tokens", type=int, default=500)

    p_list = sub.add_parser("list", help="列出可用模型")
    p_list.add_argument("--profile", default="siliconflow", choices=["siliconflow", "moonshot"])
    p_list.add_argument("--tier", type=int, help="筛选层级")

    p_models = sub.add_parser("models", help="按层级显示所有模型")
    p_models.add_argument("--profile", default="siliconflow", choices=["siliconflow", "moonshot"])

    args = parser.parse_args()
    if args.cmd == "route":
        cmd_route(args)
    elif args.cmd == "list":
        cmd_list(args)
    elif args.cmd == "models":
        cmd_models(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
