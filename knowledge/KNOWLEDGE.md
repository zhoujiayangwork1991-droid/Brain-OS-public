# Knowledge 模块

书签、研究、学习笔记的知识库。

## 结构

| 目录 / 文件 | 用途 |
|------------|------|
| `bookmarks/index.jsonl` | 网络书签（仅追加） |
| `learning/` | 学习笔记、研究报告 |

## 常见动作

- 「收藏这个 / 保存链接」→ 追加到 `bookmarks/index.jsonl`
- 「学习新知识 / 读书」→ 在 `learning/` 下建立课题笔记

## 书签格式

```
{"date": "YYYY-MM-DD", "url": "...", "title": "...", "tags": ["..."], "note": "为什么收藏"}
```
