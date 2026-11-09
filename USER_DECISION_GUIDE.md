# 用户决策指南

**1分钟快速决策**

---

## 🔴 核心澄清

**「研报」是什么？**
- ✗ 不是券商研报PDF
- ✓ 是LLM生成的投资分析报告（需LLM API Key和费用）

**仓库能提供什么？**
- ✓ 17个免费数据接口（K线/财报/新闻/龙虎榜/解禁等）
- ✗ 无券商研报下载
- ✗ 无公告原文下载

---

## 🎯 三选一决策

### 选项1：只要数据（✅ 推荐）

**适合**：
- "查天孚通信数据"
- "找中际旭创财报"
- 数据验证/回测输入

**方案**：按需CLI（无LLM，轻量，免费）

**使用**：
```bash
python data_cli.py all 300308
```

**费用**：免费  
**LLM**：不需要  
**复杂度**：低

---

### 选项2：要LLM分析报告

**适合**：
- 需要多角色分析
- 需要Bull/Bear辩论
- 需要投资建议

**方案**：现有CLI/Web UI

**使用**：
```bash
# 配置LLM
MINIMAX_API_KEY=sk-xxx

# 运行
tradingagents analyze
```

**费用**：LLM API计费（每次30-50次调用）  
**LLM**：必须  
**复杂度**：中

---

### 选项3：要券商研报

**适合**：
- 需要卖方研报PDF
- 需要分析师评级

**方案**：**仓库无此能力**

**替代**：
- 接入Wind/Choice（付费）
- 爬取券商官网（合规性待确认）

**费用**：专业数据源费用  
**LLM**：不需要  
**复杂度**：高

---

## 📦 如何开始（选项1）

### 在原电脑：

1. 克隆仓库：
```bash
git clone https://github.com/simonlin1212/TradingAgents-astock.git
cd TradingAgents-astock
```

2. 安装依赖：
```bash
pip install -e .
```

3. 复制CLI工具：
- 从 `/workspace/data_cli.py` 复制到仓库根目录

4. 运行：
```bash
python data_cli.py basic 300308
```

### 完整命令：

```bash
# 基础信息
python data_cli.py basic 300308

# 财务报表
python data_cli.py financial 300308

# 资金流+龙虎榜
python data_cli.py flow 300308

# 事件+新闻
python data_cli.py events 300308

# 完整数据
python data_cli.py all 300308

# JSON输出
python data_cli.py json 300308 -o output.json
```

---

## ⚠️ 注意事项

1. **数据窗口限制**：
   - 资金流：6个月（东财接口限制）
   - EPS：仅当前快照（同花顺限制）

2. **连接稳定性**：
   - mootdx（TCP K线）：云环境可能不稳
   - 新浪HTTP备源：稳定

3. **防前视**：
   - 新浪三表：✓ 已实现
   - 其他数据：需自行判断

4. **不干扰现有工作流**：
   - ✓ 按需调用，不常驻
   - ✓ 不写入你的目录
   - ✓ 可选独立缓存

---

## ❓ 需要你决定的

1. **选哪个方案？**
   - [ ] 选项1：只要数据
   - [ ] 选项2：要LLM分析
   - [ ] 选项3：要券商研报（仓库无）

2. **部署在哪？**
   - [ ] Grok Bot电脑
   - [ ] 原电脑
   - [ ] 其他服务器

3. **缓存策略？**
   - [ ] 使用仓库缓存（`~/.tradingagents/cache/`）
   - [ ] 自定义位置
   - [ ] 不缓存

---

## 📞 下一步

**如选择选项1（推荐）**：
1. 在原电脑克隆仓库
2. 复制 `data_cli.py`
3. 测试：`python data_cli.py basic 300308`

**如选择选项2**：
1. 配置LLM API Key
2. 运行：`tradingagents analyze`

**如选择选项3**：
1. 评估付费数据源
2. 接入Wind/Choice等

---

**决策完成？立即可用。**
