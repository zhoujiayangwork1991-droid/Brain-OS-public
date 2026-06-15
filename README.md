# Brain OS — 个人操作系统框架

> A personal "operating system" for working with AI assistants — structured as modules + skills + a memory layer.
> 一个把「个人知识 / 身份 / 目标 / 记忆」结构化、并让 AI 助手按需路由加载的框架骨架。

这是一个**框架骨架（sanitized skeleton）**：保留了完整的架构、模块结构、路由规则和一组通用技能定义，**不含任何个人数据、联系人、案例或密钥**。所有需要填入个人信息的地方都是占位符，照着填即可变成你自己的 Brain OS。

## 核心理念

1. **模块化数据层** — 11 个模块（身份 / 记忆 / 运营 / 内容 / 知识 / 人脉 / 品牌 / 模板 / 技能 / 自动化 / 个人品牌），每个模块自带一份指令文件。
2. **按需路由，上下文节俭** — 入口 `CLAUDE.md` 维护一张路由表，AI 只加载当前任务需要的模块，绝不一次全量加载。
3. **技能即工作流** — `skills/` 下每个技能是一份「目标 → 步骤 → 输出格式」的详细工作流定义，通过触发词调用。
4. **记忆沉淀** — 每次对话抽取 fact 进入临时池 `memory/fact.jsonl`，定期通过「整理记忆」技能归档到各模块。
5. **纯文本、无构建步骤** — 全部是 Markdown + JSONL + YAML，可读、可 diff、可版本控制。

## 目录结构

```
.
├── CLAUDE.md           # 总入口：规则 + 模块路由表
├── AGENT.md            # 核心铁律 + 触发词决策表
├── ARCHITECTURE.md     # 架构说明（数据层 / 方法层 / 执行层）
├── identity/           # 身份：单一真相源（占位模板）
├── memory/             # 记忆：fact 临时池 + 工作日志
├── operations/         # 运营：目标 + 进度
├── content/            # 内容创作流程
├── knowledge/          # 知识库
├── network/            # 人脉
├── personal-brand/     # 个人品牌：声音指南
├── brand/              # 品牌资产
├── templates/          # 内容模板
├── skills/             # 通用技能定义
└── automation/         # 自动化流程
```

## 快速开始

1. Clone 本仓库，作为你 AI 助手（如 Claude Code）的工作目录。
2. 把 `identity/me.template.md` 复制为 `identity/me.md`，填入你自己的信息。
3. 按 `CLAUDE.md` 的路由表使用；对话中产生的事实会沉淀到 `memory/fact.jsonl`。
4. 在 `skills/` 下按现有技能的格式添加你自己的技能。

## 包含的通用技能

| 技能 | 触发词 | 说明 |
|------|--------|------|
| make-slides | `/make-slides [主题]` | 用 python-pptx 生成 PPT |
| video-learning | `/视频学习 [URL]` | 视频 → 学习课题 |
| valuation | `/估值 [公司]` | 企业估值（DCF/DDM/P-E 等） |
| find-skills | `/find-skills [需求]` | 从开放生态搜索安装技能 |
| 整理记忆 | `/整理记忆` | fact 临时池 → 各模块归档 |

## 说明

- 本框架由作者从个人实际使用的系统中**脱敏导出**，仅保留可复用的结构与方法。
- 不构成任何专业建议；技能定义中的领域内容仅为模式示例。
- License: MIT。
