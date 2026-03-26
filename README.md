# model-router-mcp (MCP Router Demo, no API keys)

**English** | [中文](README.zh.md)

## What

This is a **Model Router MCP Demo**: given a user task (optionally with images), it outputs **OpenClaw-compatible model references** (`openclaw_model_id` / `openclaw_route_tag`) and a fallback chain so the **host agent** can call a real model in the **next** step.

This repo also includes a Cursor / OpenClaw Skill guide: [`skills/silicon-router/SKILL.md`](skills/silicon-router/SKILL.md) (how to trigger routing constraints — **not** an MCP tool name).

## No-keys guarantee

This demo **does not call** SiliconFlow / Moonshot provider APIs. You do **not** need `SILICONFLOW_API_KEY`, `MOONSHOT_API_KEY`, or any provider keys in this demo.

## How to run (CLI)

From the repository root:

```bash
python3 -B siliconflow_router/router_cli.py route "帮我设计缓存策略"
python3 -B siliconflow_router/router_cli.py route "复杂推理题" --profile moonshot
python3 -B siliconflow_router/router_cli.py list --profile moonshot --tier 1
python3 -B siliconflow_router/router_cli.py models --profile siliconflow
```

## How to run (MCP)

Install dependencies (only required to run the MCP server):

```bash
pip install -r siliconflow_router/requirements.txt
```

The MCP server speaks **stdio** (your host agent launches it as a subprocess). Optional env **`ROUTER_PROFILE`**: `siliconflow` (default) or `moonshot`, used as the default registry when `profile` is not passed explicitly.

```bash
python3 -B siliconflow_router/server.py
```

MCP tools:

- `route_task` — analyze the task and recommend a model (OpenClaw contract output)
- `set_mode` — set routing mode (`auto` / `power` / `fast` / `code` / `vision`)
- `get_status` — current default profile and mode
- `list_models` — list models by profile / tier

## Output contract (`route_task`)

`route_task` returns JSON the host can parse:

- `decision.openclaw_model_id` — `siliconflow/<id>` or `moonshot/<id>`
- `decision.openclaw_route_tag` — `[[OPENCLAW_ROUTE_MODEL:<openclaw_model_id>]]` (optional; if the host supports it, may override provider/model)
- `routing.reason` — why this route was chosen (intent + strategy)
- `cost_estimate` — rough input/output/total (demo contract)
- `fallback_chain` — fallback candidates as `openclaw_model_id` values

## OpenClaw integration

The host agent may:

- Switch models using `decision.openclaw_model_id` directly
- If supported, inject `decision.openclaw_route_tag` into prompts/config to override provider/model for that run

## License + security

The open-source code does not ship provider API keys and does not make outbound network calls during routing.

License: MIT
