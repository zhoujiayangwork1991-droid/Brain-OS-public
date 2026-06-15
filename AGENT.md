# Agent 核心规则

## 7 条铁律

1. **上下文节俭** — 只加载任务所需的模块，不贪多
2. **仅追加日志** — 所有 JSONL 文件只能 append，不能 rewrite。删除通过 `"status": "archived"` 实现
3. **先查后写** — 创建内容前，先检索已有素材库，不重复造轮子
4. **单一信息源** — 事实只在一个地方定义
5. **说人话** — 参考 `personal-brand/voice-guide.md`，使用你的声音
6. **复利优先** — 每次交互都要问：这能沉淀下来吗？
7. **ROI 驱动** — 不做低 ROI 的事

## 决策表

| 用户说 | 执行动作 |
|-------|---------|
| 「记录选题」「我有一个想法」 | → 追加到 `content/ideas.jsonl` |
| 「写文章」「写博客」 | → 加载 `personal-brand/` + `content/CONTENT.md` + `templates/` |
| 「周回顾」「本周总结」 | → 加载 `automation/weekly-review.md` |
| 「记录一个决策」 | → 追加到 `memory/decisions.jsonl` |
| 「记录经历」 | → 追加到 `memory/experiences.jsonl` |
| 「联系人」「加一个人」 | → 追加到 `network/contacts.jsonl` |
| 「收藏这个」「保存链接」 | → 追加到 `knowledge/bookmarks/index.jsonl` |
| 「设定目标」 | → 编辑 `operations/goals.yaml` |
| `/make-slides [主题]`、「做PPT」 | → 加载 `skills/make-slides.md` |
| `/video-learning [URL]`、`/视频学习 [URL]` | → 加载 `skills/video-learning.md` |
| `/估值 [公司]`、`/valuation [公司]` | → 加载 `skills/valuation/SKILL.md` |
| `/find-skills [需求]` | → 加载 `skills/find-skills/SKILL.md` |
| `/整理记忆` | → 加载 `skills/整理记忆.md`，将 fact.jsonl 归档到各模块 |

> 添加你自己的技能：在 `skills/` 下新建技能文件，在 `skills/SKILLS.md` 登记触发词，并在本表加一行。
