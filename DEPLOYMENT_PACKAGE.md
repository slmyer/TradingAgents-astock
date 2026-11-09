# 可移植到原电脑的文件清单

**目标**：在原电脑复现按需数据获取能力

---

## 📦 方案1：最小打包（仅CLI）

**适合**：只需要数据CLI，不需要完整仓库

### 必需文件（从云VM复制）：

```
data_cli.py                              # 数据CLI主程序
```

### 依赖（从仓库）：

```
tradingagents/dataflows/a_stock.py       # 17个数据接口
tradingagents/dataflows/interface.py     # 接口抽象层
tradingagents/dataflows/utils.py         # 工具函数
tradingagents/__init__.py                # 包初始化
```

### 安装步骤：

1. **克隆仓库**（获取依赖）：
```bash
git clone https://github.com/simonlin1212/TradingAgents-astock.git
cd TradingAgents-astock
```

2. **安装依赖**：
```bash
pip install -e .
```

3. **复制CLI工具**：
```bash
# 从云VM或本评估结果中复制
cp /path/to/data_cli.py ./
```

4. **测试**：
```bash
python data_cli.py basic 300308
```

---

## 📦 方案2：完整仓库（含LLM能力）

**适合**：需要完整功能（数据+LLM分析）

### 安装步骤：

1. **克隆仓库**：
```bash
git clone https://github.com/simonlin1212/TradingAgents-astock.git
cd TradingAgents-astock
```

2. **安装依赖**：
```bash
pip install -e .

# 若需Gemini（可选）：
pip install --no-deps "langchain-google-genai>=4.0.0"
pip install "google-genai>=1.53.0" "httpx>=0.28.1"

# 若需Claude订阅覆盖（可选）：
pip install -e ".[agentsdk]"
```

3. **配置LLM**（若需要LLM分析）：
```bash
# 创建 .env 文件
echo "MINIMAX_API_KEY=sk-xxx" > .env
```

4. **测试数据CLI**：
```bash
python data_cli.py basic 300308
```

5. **测试LLM分析**（可选）：
```bash
tradingagents analyze
# 或
tradingagents-web
```

---

## 📂 云VM文件路径

**本次评估生成的文件**：

| 文件 | 路径 | 说明 |
|------|------|------|
| **数据CLI** | `/workspace/data_cli.py` | 主程序 |
| **能力审计** | `/workspace/capability_audit.py` | 能力展示 |
| **快速测试** | `/workspace/quick_data_test.py` | HTTP源测试 |
| **完整评估** | `/workspace/CAPABILITY_ASSESSMENT.md` | 详细报告 |
| **决策指南** | `/workspace/USER_DECISION_GUIDE.md` | 1分钟决策 |
| **本文档** | `/workspace/DEPLOYMENT_PACKAGE.md` | 部署说明 |

**前期评估文件**（参考）：

| 文件/目录 | 路径 | 说明 |
|-----------|------|------|
| **1年标准评估** | `/workspace/final_assessment_evidence/` | 数据源评估 |
| **证据矩阵** | `/workspace/final_assessment_evidence/证据矩阵.csv` | 对比表 |

---

## 🔧 最小依赖（仅数据CLI）

```
Python >= 3.10
mootdx
requests
pandas
```

**安装**：
```bash
pip install mootdx requests pandas
```

---

## ⚠️ 重要说明

### 1. 不在Grok Bot电脑运行
- 当前评估在云VM完成
- **未在Grok Bot电脑clone或部署**
- 需用户自行决定部署位置

### 2. 数据CLI无LLM依赖
- `data_cli.py` 仅需数据依赖（mootdx/requests/pandas）
- 不需要LangChain / LangGraph / LLM SDK
- 不调用LLM，不产生费用

### 3. 仓库完整功能需LLM
- 若需LLM分析报告：必须配置API Key
- 每次分析30-50次LLM调用
- 产生API费用或消耗订阅额度

### 4. 券商研报能力
- **仓库无券商研报接口**
- 需接入付费数据源（Wind/Choice）
- 或自行爬取（合规性待确认）

---

## 📋 复制步骤（推荐）

### 在原电脑：

1. **克隆仓库**：
```bash
git clone https://github.com/simonlin1212/TradingAgents-astock.git
cd TradingAgents-astock
```

2. **安装依赖**：
```bash
pip install -e .
```

3. **从云VM下载CLI**：
```bash
# 方法1：直接从本评估commit拉取
git pull origin main

# 方法2：手动复制
# 复制 /workspace/data_cli.py 到仓库根目录
```

4. **测试**：
```bash
# 测试数据获取
python data_cli.py basic 300308

# 测试完整数据
python data_cli.py all 300308

# 测试JSON输出
python data_cli.py json 300308 -o test_output.json
```

5. **（可选）配置LLM**：
```bash
# 仅当需要LLM分析报告时
echo "MINIMAX_API_KEY=sk-xxx" > .env
tradingagents analyze
```

---

## 🚀 快速验证

### 验证1：数据CLI可用

```bash
python data_cli.py basic 300308
```

**预期**：显示K线和基本面数据

### 验证2：完整数据获取

```bash
python data_cli.py all 300308
```

**预期**：显示基础信息+财报+资金流+事件

### 验证3：JSON输出

```bash
python data_cli.py json 300308 -o test.json
cat test.json | head -50
```

**预期**：生成JSON文件，包含所有数据

---

## ❓ 故障排查

### 问题1：`ModuleNotFoundError: No module named 'tradingagents'`

**原因**：未安装仓库依赖

**解决**：
```bash
pip install -e .
```

### 问题2：mootdx连接超时

**原因**：云环境或网络问题

**解决**：
- 使用新浪HTTP备源（自动切换）
- 或修改 `a_stock.py` 优先使用新浪

### 问题3：东财接口限流

**原因**：请求过快

**解决**：
- 仓库已内置限流（1秒/次）
- 设置环境变量：`export EM_MIN_INTERVAL=1.5`

### 问题4：找不到 `data_cli.py`

**原因**：未从云VM复制

**解决**：
```bash
# 拉取最新commit
git pull origin main

# 或手动复制文件内容
```

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| `CAPABILITY_ASSESSMENT.md` | 完整能力评估 |
| `USER_DECISION_GUIDE.md` | 1分钟决策指南 |
| `README.md` | 仓库完整文档 |
| `final_assessment_evidence/` | 数据源1年评估 |

---

## ✅ 部署完成检查清单

- [ ] 仓库已克隆
- [ ] 依赖已安装（`pip install -e .`）
- [ ] `data_cli.py` 已复制到仓库根目录
- [ ] 测试基础功能（`python data_cli.py basic 300308`）
- [ ] 测试完整功能（`python data_cli.py all 300308`）
- [ ] （可选）LLM已配置（`.env`）
- [ ] （可选）测试LLM分析（`tradingagents analyze`）

---

**部署包准备完成**  
**最后更新**: 2026-11-09
