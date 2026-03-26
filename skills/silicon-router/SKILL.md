---
name: silicon-router
description: "智能模型路由：仅输出 OpenClaw 模型引用（MCP/CLI 路由推荐 Demo，无密钥版）。"
metadata:
  {
    "openclaw": { "emoji": "🧭" }
  }
---

# 智能路由 (silicon-router)

根据任务内容自动推荐模型，支持两条 `profile`：

| profile | 说明 |
|---------|------|
| `siliconflow`（默认） | 输出 `siliconflow/<id>` 的模型引用 |
| `moonshot` | 输出 `moonshot/<id>` 的模型引用（仅用于 OpenClaw 路由推荐） |

## 强制执行规则（重要）

- `silicon-router` 是 Skill 名称，不是可直接调用的 tool 名。
- 禁止发起 `toolCall: silicon-router`（该工具不存在，会报 `Tool silicon-router not found`）。
- 触发本技能后，必须先通过 **CLI** 或（你宿主已接入时）**MCP** 完成路由，再给用户回复。
- 若未完成路由，不得直接输出最终答案。

## No-keys guarantee（开源范围）

本 Demo **不调用** SiliconFlow / Moonshot provider API；路由阶段只做意图识别与模型表匹配，因此不需要任何 API Key。

## CLI 路由工具

路由脚本路径：`siliconflow_router/router_cli.py`（在 OpenClaw 仓库根目录下执行）

### 分析任务 → 推荐模型（默认 SiliconFlow）

```bash
python3 -B siliconflow_router/router_cli.py route "用户的问题或任务描述"
```

### 仅 Moonshot 官方（输出 `moonshot/<id>`）

```bash
python3 -B siliconflow_router/router_cli.py route "复杂推理题" --profile moonshot
```

包含图像、优先级等同原参数：

```bash
python3 -B siliconflow_router/router_cli.py route "分析架构图" --image --profile moonshot
python3 -B siliconflow_router/router_cli.py route "简单问题" --priority speed --profile siliconflow
```

## 输出字段（用于 OpenClaw）

- `openclaw_model_id`：形如 `siliconflow/<id>` 或 `moonshot/<id>`
- `openclaw_route_tag`：形如 `[[OPENCLAW_ROUTE_MODEL:<openclaw_model_id>]]`；若宿主支持该语义，可用于覆盖本次运行的 provider/model

## MCP 路由（可选）

若你的宿主已接入 `siliconflow_router/server.py` 作为 MCP：

- `route_task`：根据 `query` 推荐模型（可选 `profile`：`siliconflow | moonshot`；可选 `has_image`、`priority`）
- 默认 profile 可由环境变量 `ROUTER_PROFILE` 指定
- `list_models`：可传 `profile`/`tier` 查看模型表
- `set_mode` / `get_status`：查看/切换路由模式

## 使用建议

调用路由后，根据返回的 `openclaw_model_id` 告知用户建议切换的模型；若需会话级强制路由，可把 `openclaw_route_tag` 写入系统提示。

