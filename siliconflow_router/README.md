# siliconflow_router（MCP/CLI 路由 Demo）

该目录提供一个 **“只做路由推荐”** 的模型路由实现：根据用户输入意图输出 OpenClaw 兼容的模型引用（`openclaw_model_id` / `openclaw_route_tag`），路由阶段 **不发起 provider API 请求**。

## 两个 profile

- `siliconflow`：输出形如 `siliconflow/<id>` 的模型引用
- `moonshot`：输出形如 `moonshot/<id>` 的模型引用（仅指 Open Platform / Kimi 官方模型 id）

## No-keys guarantee

Demo 不需要 `SILICONFLOW_API_KEY` / `MOONSHOT_API_KEY`；代码只进行意图识别与模型表匹配。

## 快速命令（CLI）

在仓库根目录执行：

```bash
python3 -B siliconflow_router/router_cli.py route "你好" --profile siliconflow
python3 -B siliconflow_router/router_cli.py route "复杂推理题" --profile moonshot
python3 -B siliconflow_router/router_cli.py list --profile moonshot --tier 1
```

## MCP（stdio）

运行：

```bash
python3 -B siliconflow_router/server.py
```

（由你的 MCP 宿主 agent 按 stdio 方式接入）

MCP 工具：

- `route_task`：分析任务并推荐模型，输出路由契约
- `set_mode`：`auto/power/fast/code/vision` 模式切换（可选强制指定模型）
- `get_status`：查看默认 profile 与当前模式
- `list_models`：按 profile/层级列出模型表

## route_task 输出字段（契约摘要）

- `decision.openclaw_model_id`：`siliconflow/<id>` 或 `moonshot/<id>`
- `decision.openclaw_route_tag`：`[[OPENCLAW_ROUTE_MODEL:<openclaw_model_id>]]`
- `routing.reason`：路由原因（意图类型/复杂度 + 策略）
- `cost_estimate`：成本预估（Demo 版用于展示契约）
- `fallback_chain`：兜底候选的 `openclaw_model_id` 列表

## 依赖

仅当你运行 MCP server 时需要安装：

```bash
pip install -r siliconflow_router/requirements.txt
```
