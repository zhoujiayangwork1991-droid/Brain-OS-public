# Skill: make-slides

## Trigger
`/make-slides [主题或描述]`

Examples:
- `/make-slides 招股书中 Key Factors 章节的起草规则`
- `/make-slides 解释量子计算的基本概念，4张幻灯片`
- `/make-slides [任意主题] [可选：X张幻灯片]`

## Defaults
- **幻灯片数量**：4 张（如未指定）
- **配色方案**：深蓝(#1B2A4A) + 金色(#C9A02B) 专业商务风格
- **尺寸**：13.33 × 7.5 英寸（16:9 宽屏）
- **输出格式**：`.pptx` 文件，保存到当前工作目录
- **语言**：标题和内容根据用户输入语言决定（默认中文）

## Parameters
- **主题**：任何你想制作幻灯片的内容（必填）
- **张数**：可选，例如"3张"、"6张幻灯片"（默认 4 张）
- **风格**：可选，"简洁"/"密集"/"图表为主"等（默认为结构化信息卡片风格）

## Workflow

### Step 1 — 理解内容结构
分析用户的主题，规划幻灯片结构：
- **第 1 张**：核心问题 / 概念导入（设置情境，给出关键答案）
- **第 2 张**：分类 / 框架（用 2-4 列或矩阵呈现主要维度）
- **第 3 张**：对比 / 细节（通用 vs 具体 / 一般原则 vs 案例）
- **第 4 张**：案例 / 总结（真实例子 2×2 布局，或关键结论）

如果用户指定了不同张数，相应调整结构。

### Step 2 — 生成 Python 脚本

使用 `python-pptx` 生成幻灯片，遵循以下代码结构规范：

**颜色常量（固定，不修改）：**
```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

NAVY   = RGBColor(0x1B, 0x2A, 0x4A)   # 深蓝（主背景/标题栏）
GOLD   = RGBColor(0xC9, 0xA0, 0x2B)   # 金色（强调/分隔线）
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT  = RGBColor(0xF2, 0xF4, 0xF8)   # 浅灰蓝（幻灯片背景）
MID    = RGBColor(0x2A, 0x60, 0xA8)   # 蓝色（分类色1）
GREEN  = RGBColor(0x1A, 0x7A, 0x5A)   # 绿色（分类色2）
AMBER  = RGBColor(0xC0, 0x60, 0x10)   # 琥珀色（分类色3）
PURPLE = RGBColor(0x62, 0x30, 0x9A)   # 紫色（分类色4）
DARK   = RGBColor(0x1B, 0x2A, 0x4A)   # 深色文字
GREY   = RGBColor(0x55, 0x65, 0x78)   # 灰色（注释/副文本）
LGREY  = RGBColor(0xE0, 0xE4, 0xEC)   # 浅灰（边框）
```

**必须使用的三个基础函数（从参考实现复制，不修改）：**
```python
def R(slide, l, t, w, h, fill, line=None):
    """添加矩形色块"""
    s = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    s.fill.solid(); s.fill.fore_color.rgb = fill
    if line: s.line.color.rgb = line
    else: s.line.fill.background()
    return s

def T(slide, l, t, w, h, text, size, bold=False, color=WHITE,
      align=PP_ALIGN.LEFT, italic=False):
    """添加文本框"""
    b = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    b.word_wrap = True
    tf = b.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold
    r.font.italic = italic; r.font.color.rgb = color
    return b

def header(slide, title, sub=None):
    """每张幻灯片的标准顶部标题栏"""
    R(slide, 0, 0, 13.33, 1.45, NAVY)
    R(slide, 0, 1.45, 13.33, 0.06, GOLD)   # 金色分隔线
    T(slide, 0.4, 0.12, 12.5, 0.74, title, 26, bold=True, color=WHITE)
    if sub:
        T(slide, 0.4, 0.86, 12.5, 0.48, sub, 12, color=RGBColor(0xBB,0xCC,0xEE))
```

**每张幻灯片的结构模板：**
```python
prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

s1 = prs.slides.add_slide(BLANK)
R(s1, 0, 0, 13.33, 7.5, LIGHT)                    # 背景
header(s1, "标题", "副标题 · 说明文字")             # 标题栏
# ... 内容区域从 y=1.6 开始，底部留到 y=7.3
```

**内容区域可用高度：** y 从 1.62 开始，到 7.3 结束，共 5.68 英寸。
**内容区域宽度：** x 从 0.35 开始，到 13.0 结束，共 12.65 英寸。

### Step 3 — 执行脚本

将脚本保存为临时文件并执行：
```bash
python [临时脚本路径]
```

脚本执行后输出 `.pptx` 文件到当前工作目录。

### Step 4 — 向用户报告

告知用户：
- 文件名和保存路径
- 幻灯片共 X 张，分别涵盖哪些内容（一句话概括每张）

## 参考实现

已有生成案例：`Key_Factors_Financial_Performance.pptx`（招股书 Key Factors 章节，4 张幻灯片），可用于理解布局惯例和代码模式。

## Error Handling

| 错误 | 原因 | 修复 |
|-----|------|-----|
| `ModuleNotFoundError: pptx` | 未安装依赖 | `pip install python-pptx` |
| 文本溢出/重叠 | 内容过多 | 缩小字号或拆分到更多幻灯片 |
| 中文显示方块 | 系统字体问题 | 在 T() 中显式设置 `r.font.name = "微软雅黑"` |

## Output

保存路径：`[当前工作目录]/[主题slug]-slides.pptx`
（若无法自动确定，保存为 `output-slides.pptx`）
