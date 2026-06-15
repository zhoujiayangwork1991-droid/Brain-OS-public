# Skill: find-skills

> 来源：https://skills.sh/vercel-labs/skills/find-skills
> 安装：`npx skills add https://github.com/vercel-labs/skills --skill find-skills`

## 用途

帮助用户从开放生态中**搜索、验证和安装**新的 agent 技能包。

## 触发场景

以下情况部署此技能：
- 用户问"怎么做 X"，但现有技能库没有覆盖
- 用户要求为特定领域寻找工具（设计、测试、部署等）
- 用户想扩展 agent 能力
- 需要专门工作流但不确定从哪里找

## 核心 CLI 命令

```bash
npx skills find [关键词]        # 按关键词搜索技能
npx skills add <package>        # 从 GitHub 或其他来源安装
npx skills check                # 查看可用更新
npx skills update               # 刷新所有已安装技能
```

## 工作流

### Step 1 — 搜索

```bash
npx skills find [用户描述的需求关键词]
```

优先查 skills.sh 排行榜，再做定向搜索。

### Step 2 — 质量验证

展示候选技能时，必须包含以下信息：

| 字段 | 说明 |
|------|------|
| 技能名称 | skill name |
| 安装量 | 优先选 1K+ 安装；低于 100 要谨慎 |
| 来源 | 可信来源：vercel-labs、anthropics、microsoft |
| GitHub Stars | 低于 100 星需提示用户 |
| 安装命令 | `npx skills add ...` |
| 链接 | skills.sh 页面地址 |

### Step 3 — 安装

```bash
npx skills add <package-url> --skill <skill-name>
```

安装后将技能文件写入 `skills/` 并更新 `SKILLS.md` 索引。

## 统计信息（截至 2026-03）

- 周安装量：636.2K
- GitHub Stars：10.9K
- 首次收录：2026-01-26
- 安全审计：✅ Agent Trust Hub / Socket 通过；⚠️ Snyk 警告
