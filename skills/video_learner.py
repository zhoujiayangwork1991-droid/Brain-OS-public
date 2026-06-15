#!/usr/bin/env python3
"""
视频学习工具 (Video Learner)
----------------------------
功能：从在线视频（YouTube、Bilibili 等）提取内容，生成结构化学习摘要。

使用方式（Claude 通过 Bash 调用）：
  python video_learner.py --url "https://youtube.com/..." [--lang zh] [--output json]

依赖安装：
  pip install google-genai yt-dlp

API Key 配置（任选其一）：
  - 环境变量 GEMINI_API_KEY
  - 或在此文件同目录创建 .env 文件，写入 GEMINI_API_KEY=xxx
"""

import sys
import json
import argparse
import os
import re
import subprocess
import tempfile
from pathlib import Path

# ── 加载 .env（如果存在）────────────────────────────────────────────────────
_env_file = Path(__file__).parent / ".env"
if _env_file.exists():
    for line in _env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


# ────────────────────────────────────────────────────────────────────────────
# 工具函数
# ────────────────────────────────────────────────────────────────────────────

def log(msg: str):
    """写到 stderr，不影响 stdout 的 JSON 输出。"""
    print(f"[video_learner] {msg}", file=sys.stderr)


def is_youtube(url: str) -> bool:
    return "youtube.com" in url or "youtu.be" in url


def is_bilibili(url: str) -> bool:
    return "bilibili.com" in url or "b23.tv" in url


# ────────────────────────────────────────────────────────────────────────────
# 方法一：Gemini 直接读 YouTube URL（多模态）
# ────────────────────────────────────────────────────────────────────────────

GEMINI_ANALYSIS_PROMPT = """你是一位专业的学习顾问。请仔细分析这个视频，并以 JSON 格式返回以下内容（必须是合法 JSON，不加任何 markdown 代码块）：

{
  "title": "视频标题",
  "platform": "YouTube/Bilibili/其他",
  "duration_estimate": "大约时长（如 '20分钟'）",
  "language": "视频主要语言",
  "summary": "3-5句话的内容摘要，用中文",
  "key_concepts": [
    {"concept": "概念名", "explanation": "一句话解释"},
    ...
  ],
  "timeline": [
    {"timestamp": "0:00", "topic": "话题描述"},
    {"timestamp": "5:30", "topic": "话题描述"},
    ...
  ],
  "learning_points": [
    "学完这个视频，你将能够……（可验证的具体能力）",
    ...
  ],
  "suitable_for": "适合什么基础的学习者",
  "related_topics": ["相关话题1", "相关话题2"]
}

要求：
- key_concepts 提取 5-10 个最重要的概念
- timeline 按实际内容分段，每段给出时间戳
- learning_points 写成可验证的行为能力，禁止"了解/熟悉"等模糊表述
- 所有文字字段用中文输出（title 保留原文后附中文翻译）
"""

def analyze_with_gemini_url(url: str) -> dict:
    """Gemini 2.0 Flash 直接处理 YouTube URL（需要 GEMINI_API_KEY）。"""
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        raise RuntimeError("缺少 google-genai，请运行：pip install google-genai")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("未设置 GEMINI_API_KEY 环境变量或 .env 文件")

    client = genai.Client(api_key=api_key)

    log("调用 Gemini 2.5 Flash 分析视频 URL...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_uri(file_uri=url, mime_type="video/*"),
            GEMINI_ANALYSIS_PROMPT,
        ],
    )

    text = response.text.strip()
    # 去除可能的 markdown 代码块包裹
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


# ────────────────────────────────────────────────────────────────────────────
# 方法二：yt-dlp 提取字幕 → Gemini 文本分析（fallback）
# ────────────────────────────────────────────────────────────────────────────

TRANSCRIPT_ANALYSIS_PROMPT = """你是一位专业的学习顾问。以下是一段视频的字幕文本，请分析其内容并以 JSON 格式返回（必须是合法 JSON，不加任何 markdown 代码块）：

字幕内容：
{transcript}

请返回：
{{
  "title": "{title}",
  "platform": "{platform}",
  "duration_estimate": "{duration}",
  "language": "视频主要语言",
  "summary": "3-5句话的内容摘要，用中文",
  "key_concepts": [
    {{"concept": "概念名", "explanation": "一句话解释"}},
    ...
  ],
  "timeline": [
    {{"timestamp": "大致位置", "topic": "话题描述"}},
    ...
  ],
  "learning_points": [
    "学完这个视频，你将能够……（可验证的具体能力）",
    ...
  ],
  "suitable_for": "适合什么基础的学习者",
  "related_topics": ["相关话题1", "相关话题2"]
}}

要求同上，所有文字字段用中文输出。
"""

def extract_with_ytdlp(url: str) -> dict:
    """使用 yt-dlp 提取视频元数据和字幕。"""
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise RuntimeError("未找到 yt-dlp，请运行：pip install yt-dlp")

    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = [
            "yt-dlp",
            "--skip-download",
            "--write-auto-sub",
            "--sub-langs", "zh-Hans,zh,en",
            "--convert-subs", "srt",
            "--write-info-json",
            "-o", os.path.join(tmpdir, "%(id)s.%(ext)s"),
            url
        ]
        log(f"运行 yt-dlp 提取字幕：{url}")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            log(f"yt-dlp stderr: {result.stderr[:500]}")

        info_files = list(Path(tmpdir).glob("*.info.json"))
        info = {}
        if info_files:
            info = json.loads(info_files[0].read_text(encoding="utf-8"))

        transcript = ""
        for lang in ["zh-Hans", "zh", "en"]:
            srt_files = list(Path(tmpdir).glob(f"*.{lang}.srt"))
            if srt_files:
                raw = srt_files[0].read_text(encoding="utf-8")
                transcript = re.sub(r"\d+\n\d{2}:\d{2}:\d{2}.*?\n", "", raw)
                transcript = re.sub(r"\n{2,}", "\n", transcript).strip()
                log(f"找到 {lang} 字幕，长度 {len(transcript)} 字符")
                break

        return {
            "title": info.get("title", "未知标题"),
            "duration": info.get("duration_string", "未知"),
            "platform": "YouTube" if is_youtube(url) else ("Bilibili" if is_bilibili(url) else "其他"),
            "transcript": transcript[:8000],
        }


def analyze_with_transcript(url: str) -> dict:
    """yt-dlp 提取字幕 + Gemini 文本分析。"""
    try:
        from google import genai
    except ImportError:
        raise RuntimeError("缺少 google-genai，请运行：pip install google-genai")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("未设置 GEMINI_API_KEY")

    meta = extract_with_ytdlp(url)

    if not meta["transcript"]:
        raise RuntimeError(f"无法提取字幕（视频可能未开启自动字幕）：{meta['title']}")

    client = genai.Client(api_key=api_key)

    prompt = TRANSCRIPT_ANALYSIS_PROMPT.format(
        transcript=meta["transcript"],
        title=meta["title"],
        platform=meta["platform"],
        duration=meta["duration"],
    )

    log("调用 Gemini 分析字幕文本...")
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    text = response.text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


# ────────────────────────────────────────────────────────────────────────────
# 主流程
# ────────────────────────────────────────────────────────────────────────────

def analyze_video(url: str) -> dict:
    """
    分析视频，自动选择最佳方法：
    1. YouTube → 优先用 Gemini 直接读 URL（多模态）
    2. 其他平台 / Gemini URL 失败 → yt-dlp 字幕 + Gemini 文本
    """
    errors = []

    if is_youtube(url) and os.environ.get("GEMINI_API_KEY"):
        try:
            result = analyze_with_gemini_url(url)
            result["_method"] = "gemini_url"
            result["source_url"] = url
            return result
        except Exception as e:
            log(f"Gemini URL 方法失败：{e}，尝试 yt-dlp fallback...")
            errors.append(f"gemini_url: {e}")

    try:
        result = analyze_with_transcript(url)
        result["_method"] = "ytdlp_transcript"
        result["source_url"] = url
        return result
    except Exception as e:
        errors.append(f"ytdlp_transcript: {e}")

    raise RuntimeError(f"所有分析方法均失败：{'; '.join(errors)}")


def main():
    parser = argparse.ArgumentParser(description="视频学习工具 — 提取并分析在线视频内容")
    parser.add_argument("--url", required=True, help="视频 URL（YouTube、Bilibili 等）")
    parser.add_argument("--output", choices=["json", "pretty"], default="json",
                        help="输出格式：json（机器读取）或 pretty（人类可读）")
    args = parser.parse_args()

    try:
        result = analyze_video(args.url)

        if args.output == "pretty":
            print(f"\n📹 视频标题：{result.get('title', '未知')}")
            print(f"⏱  时长：{result.get('duration_estimate', '未知')}")
            print(f"\n📝 内容摘要：\n{result.get('summary', '')}")
            print(f"\n🧠 核心概念：")
            for c in result.get("key_concepts", []):
                print(f"  · {c['concept']}：{c['explanation']}")
            print(f"\n🎯 学习成果：")
            for lp in result.get("learning_points", []):
                print(f"  · {lp}")
            print(f"\n🗂 内容时间轴：")
            for t in result.get("timeline", []):
                print(f"  [{t['timestamp']}] {t['topic']}")
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        error_output = {"error": str(e), "url": args.url}
        print(json.dumps(error_output, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
