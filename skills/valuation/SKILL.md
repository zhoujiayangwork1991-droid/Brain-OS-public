# Skill: valuation（企业估值计算）

> 方法论来源：本地《企业估值模型与计算方法指南》（请替换为你自己的参考文档路径）

## 触发词

`/valuation [公司名或股票代码]` 或 `/估值 [公司]`

Examples:
- `/valuation AAPL` — 苹果公司完整估值分析
- `/估值 比亚迪` — A股公司估值
- `/valuation 腾讯 DCF` — 指定用 DCF 模型
- `/估值 某初创公司 P/S` — 未盈利企业用市销率

---

## 估值模型选择指引

| 场景 | 推荐模型 | 原因 |
|------|---------|------|
| 成熟企业、现金流稳定 | **DCF** | 最能体现内在价值 |
| 支付稳定股利的蓝筹股 | **DDM** | 直接基于股利定价 |
| 盈利稳定、行业可比公司多 | **P/E** | 最常用、横向比较直观 |
| 银行、保险、重资产企业 | **P/B** | 反映资产净值 |
| 并购分析、资本密集型 | **EV/EBITDA** | 排除资本结构差异 |
| 高成长但亏损（SaaS/初创）| **P/S** | 无需盈利，以收入定价 |

> 实际操作：通常同时运行 2-3 个模型，交叉验证，取结果区间。

---

## 模型一：DCF（现金流折现）

**公式：**
```
V = Σ [CF_t / (1+r)^t] + TV / (1+r)^n

TV（终值）= CF_{n+1} / (r - g)
```

**参数说明：**
- `CF_t`：第 t 年自由现金流（FCF = 经营现金流 - 资本支出）
- `r`：折现率，通常用 WACC
- `n`：预测期（通常5-10年）
- `g`：永续增长率（通常取2-3%，不超过GDP增速）

**WACC 计算：**
```
WACC = E/(E+D) × Re + D/(E+D) × Rd × (1 - 税率)

Re（股权成本）= 无风险利率 + β × 市场风险溢价
```

**执行步骤：**
1. 获取近3-5年历史 FCF（来自现金流量表）
2. 预测未来5年 FCF（参考收入增速、利润率趋势）
3. 计算 WACC（查 β 值，用10年期国债收益率作无风险利率）
4. 计算终值（永续增长模型）
5. 将各年 FCF + 终值折现求和
6. 减去净负债，得股权价值；除以总股数，得每股内在价值

---

## 模型二：DDM（股利折现，戈登增长模型）

**公式：**
```
P = D1 / (r - g)
```

**参数说明：**
- `D1`：下一期预期股利（= 当前股利 × (1+g)）
- `r`：股权资本成本
- `g`：股利固定增长率

**适用条件：** 股利支付历史稳定，增长率 g < r。

---

## 模型三：相对估值（倍数法）

### P/E（市盈率）
```
目标市值 = 可比公司平均P/E × 目标公司净利润
每股价值 = 目标市值 / 总股数
```

### P/B（市净率）
```
目标市值 = 可比公司平均P/B × 目标公司净资产
```

### EV/EBITDA
```
EV = 可比公司平均EV/EBITDA × 目标公司EBITDA
股权价值 = EV - 净负债（总负债 - 现金）
```

### P/S（市销率）
```
目标市值 = 可比公司平均P/S × 目标公司营业收入
```

---

## 数据获取

### 上市公司（自动获取）

**港股/美股 → yfinance：**
```python
import yfinance as yf

ticker = yf.Ticker("AAPL")        # 美股
# ticker = yf.Ticker("0700.HK")  # 港股格式

income_stmt  = ticker.income_stmt      # 利润表
balance_sheet = ticker.balance_sheet   # 资产负债表
cash_flow    = ticker.cashflow         # 现金流量表
info         = ticker.info             # 市值、P/E、Beta 等
```

**A股 → tushare：**
```python
import tushare as ts
ts.set_token("你的token")
pro = ts.pro_api()

df = pro.income(ts_code="600519.SH", period="20231231")   # 利润表
df = pro.balancesheet(ts_code="600519.SH")                # 资产负债表
df = pro.cashflow(ts_code="600519.SH")                    # 现金流量表
```

**依赖安装：**
```bash
pip install yfinance tushare pandas
```

### 非上市/招股书项目（手动输入）

从招股书 PDF 提取财务数据：
```python
import pdfplumber

with pdfplumber.open("prospectus.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        tables = page.extract_tables()   # 财务报表表格
```

---

## 输出格式

每次估值分析输出以下结构：

```
## [公司名] 估值分析

### 数据来源与时间节点
- 财务数据截至：XXXX年XX月XX日
- 股价参考：XXX（截至XXXX）

### 模型一：DCF
- 预测FCF（5年）：[Year1, Year2, Year3, Year4, Year5]
- WACC：X.X%，永续增长率：X.X%
- 内在价值（每股）：HK$/US$ XXX
- 当前股价：XXX → 溢价/折价 XX%

### 模型二：相对估值（P/E / EV/EBITDA）
- 可比公司：[A, B, C]，行业均值：P/E = XX倍
- 目标估值：HK$/US$ XXX

### 综合结论
- 估值区间：XXX ~ XXX
- 对比当前价格：[低估 / 合理 / 高估]
- 主要不确定性：[列出2-3个影响估值的关键变量]
```

---

## 与现有工作的关联

**招股书项目：**
- 从招股书 PDF 提取财务数据时，配合 `prospectus-update` 技能的 pdfplumber 工具
- 估值分析结果可支持 IPO 定价合理性披露（Valuation Analysis 章节）

**轮次融资项目：**
- 早期公司通常用 P/S 或可比交易法
- 配合 `series-financing` 技能中的 TS/SPA 条款分析

---

## 注意事项

- DCF 对假设极度敏感：g 从 2% 改到 3%，估值可能差 30%+；务必做敏感性分析
- 相对估值依赖可比公司选择，行业选择不当结论无意义
- 招股书中的财务数据已经审计，可直接用；Pre-IPO 公司的管理层预测需要打折
- 港股18A生物科技公司通常亏损，DCF意义有限，常用 Pipeline NPV 或 P/S 估值
