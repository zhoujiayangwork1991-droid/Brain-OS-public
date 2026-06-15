# 周回顾流程

**触发**：「周回顾」「本周总结」或每周定时。

## 步骤

1. **读取本周数据**
   - `memory/worklog/` 本周的日志
   - `memory/fact.jsonl` 本周新增的 fact
   - `operations/progress.md` 当前进展
2. **对齐目标**
   - 对照 `operations/goals.yaml`，本周哪些 KR 有推进？哪些停滞？
3. **产出回顾**
   - 本周完成了什么（事实，不修饰）
   - 遇到的问题 / 踩的坑（可写入 `memory/failures.jsonl`）
   - 下周 1–3 个重点
4. **存档**
   - 写入 `memory/worklog/YYYY-MM-DD-weekly.md`

## 原则

- 只读不猜：基于实际日志，不编造进展
- 诚实：停滞就说停滞
