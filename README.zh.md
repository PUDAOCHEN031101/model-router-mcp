# model-router-mcp（MCP Router Demo，无密钥版）

[English](README.md) | **中文**

## What

这是 **Model Router MCP Demo**：根据用户任务意图（可选是否包含图像），输出 **OpenClaw 兼容的模型引用**（`openclaw_model_id` / `openclaw_route_tag`）与兜底链路，供宿主 agent **下一步** 再去调用真实模型。

本仓库还包含面向 Cursor / OpenClaw 的 Skill 说明：`skills/silicon-router/SKILL.md`（说明如何触发路由约束，**不是** MCP 工具名）。

## No-keys guarantee

该 Demo **不调用** SiliconFlow / Moonshot 任何 provider API，因此不需要 `SILICONFLOW_API_KEY`、`MOONSHOT_API_KEY` 等密钥，也**不要**在本 Demo 里配置 provider Key。

## How to run (CLI)

在仓库根目录执行：

```bash
python3 -B siliconflow_router/router_cli.py route "帮我设计缓存策略"
python3 -B siliconflow_router/router_cli.py route "复杂推理题" --profile moonshot
python3 -B siliconflow_router/router_cli.py list --profile moonshot --tier 1
python3 -B siliconflow_router/router_cli.py models --profile siliconflow
```

## How to run (MCP)

先安装依赖（仅运行 MCP server 时需要）：

```bash
pip install -r siliconflow_router/requirements.txt
```

MCP 使用 stdio 启动（由你的 MCP 宿主 agent 以子进程方式接入）。可选环境变量 **`ROUTER_PROFILE`**：`siliconflow`（默认）或 `moonshot`，作为未显式传 `profile` 时的默认路由表。

```bash
python3 -B siliconflow_router/server.py
```

MCP 工具名如下：

- `route_task`：分析任务并推荐模型（输出 OpenClaw 契约）
- `set_mode`：设置路由模式（`auto/power/fast/code/vision`）
- `get_status`：查询当前默认 profile 与模式
- `list_models`：按 profile/层级列出模型表

## Output contract（route_task 返回）

`route_task` 返回 JSON（宿主可直接解析其中字段）：

- `decision.openclaw_model_id`：`siliconflow/<id>` 或 `moonshot/<id>`
- `decision.openclaw_route_tag`：`[[OPENCLAW_ROUTE_MODEL:<openclaw_model_id>]]`（可选，宿主若支持则用于覆盖 provider/model）
- `routing.reason`：路由原因（意图类型/复杂度 + 策略）
- `cost_estimate`：输入/输出/总价预估（Demo 版用于展示契约）
- `fallback_chain`：兜底候选的 `openclaw_model_id` 列表

## OpenClaw 集成方式

宿主 agent 可以：

- 直接使用 `decision.openclaw_model_id` 切换模型
- 若宿主支持该语义，则在提示/配置中注入 `decision.openclaw_route_tag` 来覆盖本次运行的 provider/model

## License + Security notes

开源代码不包含任何 provider API Key，也不会在路由阶段发起外部网络请求。

License: MIT
