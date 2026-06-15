# Operations 模块

目标、任务、会议、指标的运营中枢。

## 文件

| 文件 | 用途 | 格式 |
|------|------|------|
| `goals.yaml` | 年度目标 + Key Results（从 `goals.example.yaml` 复制） | YAML |
| `progress.md` | 当日 / 当前进展 | Markdown |
| `meetings.jsonl` | 会议记录 | JSONL |
| `metrics.jsonl` | 指标追踪 | JSONL |

## 常见动作

- 「设定目标」→ 编辑 `goals.yaml`
- 「存档进度」/ `/checkpoint` → 写 `progress.md` + `memory/worklog/YYYY-MM-DD.md`
- 「周回顾」→ 加载 `automation/weekly-review.md`
- 「恢复上下文」/ `/recap` → 读取 `progress.md` + 最近 worklog + `memory/fact.jsonl`
