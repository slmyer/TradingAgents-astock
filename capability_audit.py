#!/usr/bin/env python3
"""
TradingAgents-Astock 能力全景审计
核心：搞清楚"研报"到底是什么，哪些能力可复用
"""

import sys
import os
import json
from datetime import datetime

sys.path.insert(0, '/workspace')

# ============================================================================
# 核心结论：研报能力澄清
# ============================================================================

RESEARCH_REPORT_CLARIFICATION = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                    【研报能力澄清】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TradingAgents-Astock 的"研报"是什么？

✗ 【不是】真实券商研报
  - 不会下载/获取券商卖方研报PDF
  - 不会获取研报元数据（机构/分析师/评级/目标价）
  - 仓库内**无券商研报接口**

✓ 【实际是】LLM生成的投资分析报告
  - 7个Analyst角色生成的领域报告：
    · Market Analyst (市场分析师) - 技术面
    · Social Media Analyst (舆情分析师) - 情绪面
    · News Analyst (新闻分析师) - 事件面
    · Fundamentals Analyst (基本面分析师) - 财务面
    · Policy Analyst (政策分析师) - A股特化
    · Hot Money Tracker (游资追踪师) - A股特化
    · Lockup Watcher (解禁监控师) - A股特化

  - Bull vs Bear 研究员辩论
  - Research Manager 综合研判
  - 三方风险辩论
  - Portfolio Manager 最终决策

原始数据来源（仓库已实现）：
  ✓ mootdx: OHLCV K线、财务快照
  ✓ 腾讯财经: PE/PB/市值/换手率
  ✓ 东方财富: 龙虎榜、解禁、板块行情、资金流
  ✓ 新浪财经: K线历史、财报三表
  ✓ 同花顺: EPS一致预期、热股题材
  ✓ 财联社: 全球财经快讯

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
结论：无券商研报能力，仅LLM分析报告生成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

# ============================================================================
# 数据层能力清单（17个接口）
# ============================================================================

DATA_LAYER_CAPABILITIES = [
    {
        "name": "get_stock_data",
        "description": "OHLCV K线",
        "sources": "mootdx(TCP) / 新浪(HTTP备源)",
        "fields": "开高低收/成交量/成交额",
        "window": "多年",
        "auth": "无需",
        "status": "✓ 可用",
        "tested": False,
    },
    {
        "name": "get_indicators",
        "description": "技术指标（MA/MACD/RSI/BOLL等）",
        "sources": "基于OHLCV计算",
        "fields": "20+技术指标",
        "window": "依赖OHLCV窗口",
        "auth": "无需",
        "status": "✓ 可用",
        "tested": False,
    },
    {
        "name": "get_fundamentals",
        "description": "财务快照",
        "sources": "mootdx + 腾讯",
        "fields": "PE/PB/总市值/流通市值/ROE/净利润等",
        "window": "当前快照",
        "auth": "无需",
        "status": "✓ 可用",
        "tested": False,
    },
    {
        "name": "get_balance_sheet",
        "description": "资产负债表",
        "sources": "新浪财报",
        "fields": "资产/负债/所有者权益三表",
        "window": "多年（最早2002）",
        "auth": "无需",
        "status": "✓ 可用，防前视已实现",
        "tested": False,
    },
    {
        "name": "get_cashflow",
        "description": "现金流量表",
        "sources": "新浪财报",
        "fields": "经营/投资/筹资活动现金流",
        "window": "多年（最早2002）",
        "auth": "无需",
        "status": "✓ 可用，防前视已实现",
        "tested": False,
    },
    {
        "name": "get_income_statement",
        "description": "利润表",
        "sources": "新浪财报",
        "fields": "营收/成本/利润",
        "window": "多年（最早2002）",
        "auth": "无需",
        "status": "✓ 可用，防前视已实现",
        "tested": False,
    },
    {
        "name": "get_news",
        "description": "个股新闻",
        "sources": "东财",
        "fields": "标题/正文/时间（仅文本）",
        "window": "?待查",
        "auth": "无需",
        "status": "✓ 可用（无结构化标签）",
        "tested": False,
    },
    {
        "name": "get_global_news",
        "description": "全球财经快讯",
        "sources": "财联社",
        "fields": "标题/正文/时间",
        "window": "?待查",
        "auth": "无需",
        "status": "✓ 可用",
        "tested": False,
    },
    {
        "name": "get_insider_transactions",
        "description": "龙虎榜/大宗交易",
        "sources": "东财",
        "fields": "席位/买卖金额/日期",
        "window": "近30日",
        "auth": "无需",
        "status": "✓ 可用",
        "tested": False,
    },
    {
        "name": "get_profit_forecast",
        "description": "EPS一致预期",
        "sources": "同花顺10jqka",
        "fields": "一致预期EPS",
        "window": "当前快照",
        "auth": "无需",
        "status": "⚠️ 仅当前快照，无历史",
        "tested": False,
    },
    {
        "name": "get_hot_stocks",
        "description": "热股题材",
        "sources": "同花顺10jqka",
        "fields": "股票+题材标签",
        "window": "当前",
        "auth": "无需",
        "status": "⚠️ 前轮周日测试有占位符",
        "tested": False,
    },
    {
        "name": "get_northbound_flow",
        "description": "北向资金",
        "sources": "mootdx",
        "fields": "沪/深港通流入",
        "window": "?待查",
        "auth": "无需",
        "status": "⚠️ 云环境连接不稳",
        "tested": False,
    },
    {
        "name": "get_concept_blocks",
        "description": "概念板块",
        "sources": "东财",
        "fields": "板块列表/涨跌/成交",
        "window": "当前",
        "auth": "无需",
        "status": "✓ 可用",
        "tested": False,
    },
    {
        "name": "get_fund_flow",
        "description": "个股资金流",
        "sources": "东财push2his",
        "fields": "主力/超大/大/中/小单",
        "window": "~6个月(121日)",
        "auth": "无需",
        "status": "✗ 不足1年",
        "tested": False,
    },
    {
        "name": "get_dragon_tiger_board",
        "description": "龙虎榜详细",
        "sources": "东财datacenter",
        "fields": "席位明细/机构识别",
        "window": "近30日",
        "auth": "无需",
        "status": "✓ 可用",
        "tested": False,
    },
    {
        "name": "get_lockup_expiry",
        "description": "限售解禁",
        "sources": "东财datacenter",
        "fields": "解禁日期/数量/类型",
        "window": "未来为主",
        "auth": "无需",
        "status": "✓ 可用",
        "tested": False,
    },
    {
        "name": "get_industry_comparison",
        "description": "行业对比",
        "sources": "东财",
        "fields": "同行业股票对比",
        "window": "当前",
        "auth": "无需",
        "status": "✓ 可用",
        "tested": False,
    },
]

# ============================================================================
# 三种复用方案对比
# ============================================================================

DEPLOYMENT_COMPARISON = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            【三种复用方案对比】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

方案A：按需CLI/薄数据层（推荐）
─────────────────────────────────────────────────────────
✓ 不常驻、无服务进程
✓ 不启动LLM
✓ 按需调用17个数据接口
✓ 返回真实数据+来源+日期+字段+单位
✓ 显式缓存、错误状态
✓ 轻量（仅数据依赖）

依赖：
  - mootdx (TCP K线)
  - requests (HTTP APIs)
  - pandas (数据处理)
  
LLM/数据权限：
  - 无需LLM
  - 无需API Key
  - 所有数据免费公开
  
运行维护：
  - 一次性调用
  - 无进程常驻
  - 无状态
  
缓存复用：
  - 可按需实现本地缓存
  - 不与用户现有回测缓存冲突
  
隐私：
  - 本地运行
  - 不上传数据
  
影响Grok Bot电脑：
  - 不影响（未在该电脑运行）
  
费用：
  - 免费（无LLM调用）


方案B：现有CLI/Web服务
─────────────────────────────────────────────────────────
△ 需启动Streamlit或CLI
✗ 必须配置LLM（强依赖）
✓ 可生成完整多角色分析报告
△ 较重（LangGraph + LLM clients）

依赖：
  - 方案A的所有依赖
  + LangChain / LangGraph
  + LLM SDK (openai/anthropic/等)
  + Streamlit (Web UI)
  
LLM/数据权限：
  - **必须LLM API Key**
  - 或Claude Pro/Max订阅
  - 每次分析30-50次调用
  
运行维护：
  - Web需端口（8501）
  - CLI交互式或命令行
  
缓存复用：
  - 有记忆日志（SQLite）
  - 可能与现有目录冲突
  
隐私：
  - 数据发送给LLM provider
  
影响Grok Bot电脑：
  - 若在该电脑运行会占资源
  - LLM调用产生费用
  
费用：
  - **LLM API计费**
  - 或消耗订阅额度


方案C：整套UI+多角色分析（常驻服务）
─────────────────────────────────────────────────────────
✗ 需常驻服务
✗ 公开端口（不符合要求）
✗ 强依赖LLM
✗ 最重

依赖：
  - 方案B的所有依赖
  + 可能需要反向代理
  + 进程管理（systemd/supervisor）
  
LLM/数据权限：
  - **必须LLM API Key**
  
运行维护：
  - **需常驻进程**
  - **需端口暴露**
  - 需监控/重启
  
缓存复用：
  - 共享缓存可能冲突
  
隐私：
  - 数据发送给LLM
  - 若公开端口有安全风险
  
影响Grok Bot电脑：
  - **强影响**（常驻占资源）
  
费用：
  - **持续LLM费用**
  - 或快速消耗订阅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
推荐：方案A（按需CLI/薄数据层）
理由：
  1. 用户要求不调用收费LLM、不注册、不公开端口
  2. 目标是"查天孚通信数据/找中际旭创研报"式复用
  3. 不需要多角色分析（那是LLM生成，非券商研报）
  4. 仅需数据获取能力
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

def main():
    print(RESEARCH_REPORT_CLARIFICATION)
    print()
    print(DEPLOYMENT_COMPARISON)
    print()
    print("=" * 80)
    print("数据层能力清单（17个接口）")
    print("=" * 80)
    
    for i, cap in enumerate(DATA_LAYER_CAPABILITIES, 1):
        print(f"\n{i}. {cap['name']}")
        print(f"   描述: {cap['description']}")
        print(f"   来源: {cap['sources']}")
        print(f"   字段: {cap['fields']}")
        print(f"   窗口: {cap['window']}")
        print(f"   授权: {cap['auth']}")
        print(f"   状态: {cap['status']}")
    
    print("\n" + "=" * 80)
    print("审计完成")
    print("=" * 80)

if __name__ == "__main__":
    main()
