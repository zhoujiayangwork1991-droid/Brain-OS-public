# Memory 模块

人生级别的事实沉淀。所有对话抽取的 fact 先进入临时池，再定期归档。

## 文件

| 文件 | 用途 | 格式 |
|------|------|------|
| `fact.jsonl` | **临时池**：每次对话抽取的 fact | JSONL（仅追加） |
| `experiences.jsonl` | 经历（整理后） | JSONL |
| `decisions.jsonl` | 决策记录 | JSONL |
| `failures.jsonl` | 失败 / 踩坑记录 | JSONL |
| `worklog/YYYY-MM-DD.md` | 每日工作日志 | Markdown |

## fact 抽取格式

```
{"date": "YYYY-MM-DD", "fact": "一句话事实", "source": "对话摘要", "module_hint": "模块名"}
```

`module_hint` ∈ personal-brand / content / knowledge / network / operations / identity / brand / memory / templates / skills / automation

## 归档

触发 `/整理记忆`（见 `skills/整理记忆.md`）：读取 `fact.jsonl`，按 `module_hint`
把每条归档到对应模块的数据文件，然后从临时池删除已归档条目。

## 规则

- **仅追加**：JSONL 文件只能 append，不能 rewrite
- **删除 = 标记**：用 `"status": "archived"` 而非物理删除
