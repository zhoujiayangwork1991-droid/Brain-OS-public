# Network 模块

联系人、互动、关系圈层。

## 文件

| 文件 | 用途 | 格式 |
|------|------|------|
| `contacts.jsonl` | 联系人（从 `contacts.example.jsonl` 起步） | JSONL（仅追加） |
| `interactions.jsonl` | 互动记录 | JSONL |
| `circles.yaml` | 关系圈层 | YAML |

## 常见动作

- 「加一个人 / 认识了谁」→ 追加到 `contacts.jsonl`
- 「会议准备」→ 读取该联系人的 contacts + interactions
- 人脉维护 → 加载 `automation/`（检查久未联系的人）

## 规则

- 准备会议或处理人脉时**只**加载 Network，绝不读 Content 模板
- 联系人信息属敏感数据，注意不要外泄
