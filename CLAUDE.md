# Personal Brain OS

> 这是一个个人操作系统框架。所有 AI 助手在此仓库工作时，**先读此文件**。
> 核心规则见 `AGENT.md`。

## ⚠️ 强制规则：每次对话必须抽取 Fact

每次对话结束前，必须将本次对话中的内容抽取为 fact，追加到 `memory/fact.jsonl`：

```
{"date": "YYYY-MM-DD", "fact": "...", "source": "对话摘要", "module_hint": "模块名"}
```

- **任何对话都要抽取**：学习、聊天、操作文件、问答——全部适用
- **JSONL 文件只能追加，不能覆盖** — 这是安全底线
- `module_hint` 从以下选择：personal-brand / content / knowledge / network / operations / identity / brand / memory / templates / skills / automation

## 你在和谁工作

详细的身份信息见 `identity/me.md`（从 `identity/me.template.md` 复制并填写你自己的信息）。

## 11 个模块

| # | 模块 | 目录 | 指令文件 | 内容 |
|---|------|------|---------|------|
| 1 | **Personal Brand** | `personal-brand/` | `voice-guide.md` | 声音、定位、价值观 |
| 2 | **Content Creation** | `content/` | `content/CONTENT.md` | 创意、草稿、发布流程 |
| 3 | **Knowledge Base** | `knowledge/` | `knowledge/KNOWLEDGE.md` | 书签、研究、学习 |
| 4 | **Network** | `network/` | `network/NETWORK.md` | 联系人、关系、介绍 |
| 5 | **Operations** | `operations/` | `operations/OPERATIONS.md` | 目标、任务、会议、指标 |
| 6 | **Identity** | `identity/` | `identity/me.md` | 个人身份信息 |
| 7 | **Brand** | `brand/` | `brand/assets.md` | 品牌资产 |
| 8 | **Memory** | `memory/` | `memory/MEMORY.md` | 经验、决策、失败记录 |
| 9 | **Templates** | `templates/` | `templates/TEMPLATES.md` | 内容模板 |
| 10 | **Skills** | `skills/` | `skills/SKILLS.md` | AI 技能定义 |
| 11 | **Automation** | `automation/` | `automation/AUTOMATION.md` | 自动化脚本 |

## 模块加载路由

| 任务类型 | 加载模块（仅这些） |
|---------|-------------------|
| 写内容、发帖、选题 | Personal Brand + Content + Templates |
| 收藏内容、保存书签、查书签 | Knowledge |
| 学习新知识、读书 | Knowledge |
| 设定目标、周回顾、任务管理 | Operations + Automation |
| 联系人、人脉、会议准备 | Network |
| 记录经历、决策、复盘 | Memory |
| 了解我是谁 | Identity |
| 品牌资产（头像、配色、简介） | Brand |
| 存档进度、恢复上下文 | Operations + Memory |
| 复盘、踩坑分析 | Memory |

## 核心规则

1. **不要一次加载所有模块** — 只加载当前任务需要的
2. **写内容时**：加载 Personal Brand + Content + Templates。绝不看 Network 数据
3. **准备会议时**：加载 Network。绝不看 Content 模板
4. **JSONL 文件只能追加，不能覆盖** — 这是安全底线
5. **最多两跳到达任何信息** — CLAUDE.md → 模块指令 → 具体数据
6. **技能路由强制查表** — 执行任何技能前，必须先读 `skills/SKILLS.md` 确认对应的技能文件路径，然后加载该文件。不得在其他文件中创建或发明技能定义
7. **每次对话结束前必须抽取 fact** — 见文件顶部「强制规则」

## Fact 抽取规则

- 记录本次对话中出现的**任何内容**：事实、学到的知识、做的决策、有用的信息、讨论的想法等
- 每条 fact 一行，简洁陈述，不超过 100 字
- 触发词 `/整理记忆` → 加载 `skills/整理记忆.md`，将 `fact.jsonl` 归档到各模块

## 文件格式约定

| 格式 | 用途 |
|------|------|
| JSONL | 日志数据（经历、联系人、想法、指标） |
| YAML | 配置（目标、价值观、节奏） |
| Markdown | 叙事内容（指南、草稿、研究） |
