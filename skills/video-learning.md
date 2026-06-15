# Skill: video-learning

## Trigger
`/video-learning [URL]` 或 `/视频学习 [URL]`

Examples:
- `/video-learning https://youtube.com/watch?v=xxx`
- `/视频学习 https://www.bilibili.com/video/BVxxx`
- `帮我学这个视频 [URL]`
- `把这个视频加入学习 [URL]`

## Dependencies

**工具脚本：**
`skills/video_learner.py`

**Python 依赖：**
- `google-genai`（`pip install google-genai`）
- `yt-dlp`（`pip install yt-dlp`）

**API Key：**
`GEMINI_API_KEY` — 环境变量或 `.env` 文件（位于 video_learner.py 同目录）

## Workflow

### Step 1 — 调用视频分析工具

```bash
python skills/video_learner.py --url "[URL]" --output json
```

**分析逻辑（脚本自动选择）：**
- YouTube + GEMINI_API_KEY 可用 → Gemini 2.5 Flash 直读 URL（多模态，最准确）
- 其他平台 / Gemini 失败 → yt-dlp 提取字幕 → Gemini 文本分析（fallback）

### Step 2 — 解析 JSON 输出

成功时输出包含：
```json
{
  "title": "视频标题",
  "summary": "内容摘要",
  "key_concepts": [{"concept": "...", "explanation": "..."}],
  "timeline": [{"timestamp": "0:00", "topic": "..."}],
  "learning_points": ["学完后能够…"],
  "suitable_for": "适合的学习者背景",
  "related_topics": ["..."]
}
```

若输出包含 `"error"` 字段，执行 Error Handling，不继续后续步骤。

### Step 3 — 确认用户意图

询问（一次性问清，不拆成多轮）：
- 是加入已有课题，还是创建新课题？
- 如果新课题，用什么名称作为文件夹名？（默认用视频标题中文版）

> 若用户在命令中已指定课题（如 `/视频学习 [URL] 加入"量子计算"课题`），直接跳到 Step 4。

### Step 4 — 在 Bloom 仓库创建/更新课题

**目标仓库：** `<YOUR_LEARNING_REPO>/`（在配置中指向你自己的学习笔记仓库）

**① 创建新课题（最常见情况）：**
- 在 Bloom 仓库根目录创建以课题名命名的文件夹
- 生成 `syllabus.md`：以 `learning_points` 作为核心掌握项，`key_concepts` 中的模块作为分组依据
- 生成 `01.md`（首篇格式）：
  - 开头注明视频来源：`> 本篇基于视频：[标题](URL)`
  - 正文按 `timeline` 时间轴组织，深度讲解每个 `key_concepts`
  - 不是字幕复述，而是苏格拉底式导师讲解
  - 末尾含"思考题"和"你的反馈"区

**② 加入已有课题：**
- 读取该课题的 `syllabus.md`，判断视频内容与哪些未完成掌握项相关
- 生成下一篇文档（续篇格式），覆盖对应掌握项
- 更新 `syllabus.md` 进度表格

### Step 5 — 遵守 Bloom 仓库铁律

- **每次只生成一篇文档**（无论视频多长）
- 生成后必须更新 `syllabus.md`（勾选掌握项 + 追加进度表格）
- 等用户提交反馈后，才能生成下一篇

## Error Handling

| 错误信息 | 原因 | 修复建议 |
|---------|------|---------|
| `未设置 GEMINI_API_KEY` | 缺少 API Key | 在 video_learner.py 同目录创建 `.env`，写入 `GEMINI_API_KEY=你的key` |
| `无法提取字幕` | 视频未开启自动字幕 | 暂不支持，可手动粘贴视频文字稿 |
| `yt-dlp 未找到` | 未安装 | `pip install yt-dlp` |
| `google-genai 缺少` | 未安装 | `pip install google-genai` |
| `ModuleNotFoundError` | 其他依赖缺失 | 按错误提示安装对应包 |

## Output Location

```
<YOUR_LEARNING_REPO>/
└── [课题名]/
    ├── syllabus.md
    └── 01.md
```
