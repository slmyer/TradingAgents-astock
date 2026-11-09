#!/usr/bin/env python3
"""
最小数据CLI - 无LLM模式
按股票代码返回真实数据及来源、日期、字段单位、缓存、错误状态
"""

import sys
import os
import json
from datetime import datetime, timedelta
import argparse

sys.path.insert(0, '/workspace')

from tradingagents.dataflows import a_stock

# ============================================================================
# 数据获取封装（带错误处理和元数据）
# ============================================================================

def fetch_with_metadata(func_name, *args, **kwargs):
    """
    调用数据接口并返回标准化结果
    
    返回格式：
    {
        "success": bool,
        "function": str,
        "source": str,
        "timestamp": str,
        "data": str/dict,
        "error": str (if failed),
        "fields": list,
        "date_range": dict (if applicable)
    }
    """
    result = {
        "success": False,
        "function": func_name,
        "timestamp": datetime.now().isoformat(),
    }
    
    try:
        func = getattr(a_stock, func_name)
        data = func(*args, **kwargs)
        
        result["success"] = True
        result["data"] = data
        
        # 根据函数类型添加元数据
        if func_name == "get_stock_data":
            result["source"] = "mootdx(TCP) / 新浪(HTTP备源)"
            result["fields"] = ["日期", "开盘", "收盘", "最高", "最低", "成交量", "成交额"]
            
        elif func_name == "get_fundamentals":
            result["source"] = "mootdx + 腾讯财经"
            result["fields"] = ["PE", "PB", "总市值", "流通市值", "ROE", "净利润等"]
            
        elif func_name == "get_balance_sheet":
            result["source"] = "新浪财报"
            result["fields"] = ["资产", "负债", "所有者权益"]
            result["防前视"] = "✓ 已实现"
            
        elif func_name == "get_cashflow":
            result["source"] = "新浪财报"
            result["fields"] = ["经营活动现金流", "投资活动现金流", "筹资活动现金流"]
            result["防前视"] = "✓ 已实现"
            
        elif func_name == "get_income_statement":
            result["source"] = "新浪财报"
            result["fields"] = ["营业收入", "营业成本", "净利润"]
            result["防前视"] = "✓ 已实现"
            
        elif func_name == "get_fund_flow":
            result["source"] = "东财push2his"
            result["fields"] = ["主力净流入", "超大单", "大单", "中单", "小单"]
            result["窗口限制"] = "~6个月(121日)"
            
        elif func_name == "get_news":
            result["source"] = "东财"
            result["fields"] = ["标题", "正文", "时间"]
            result["注意"] = "仅文本，无结构化利多利空标签"
            
        elif func_name == "get_dragon_tiger_board":
            result["source"] = "东财datacenter"
            result["fields"] = ["上榜日期", "席位名称", "买入金额", "卖出金额", "机构标识"]
            
        elif func_name == "get_lockup_expiry":
            result["source"] = "东财datacenter"
            result["fields"] = ["解禁日期", "解禁数量", "解禁类型", "解禁市值"]
            
        elif func_name == "get_profit_forecast":
            result["source"] = "同花顺10jqka"
            result["fields"] = ["一致预期EPS"]
            result["警告"] = "⚠️ 仅当前快照，无历史回溯"
            
        else:
            result["source"] = "未知"
            
    except Exception as e:
        result["success"] = False
        result["error"] = str(e)
        result["error_type"] = type(e).__name__
    
    return result


# ============================================================================
# CLI命令实现
# ============================================================================

def cmd_basic(ticker: str):
    """基础信息：K线+基本面快照"""
    print(f"\n{'='*80}")
    print(f"【基础信息】{ticker}")
    print(f"{'='*80}\n")
    
    # 1. 最近30天K线
    print("1. K线数据（最近30天）")
    print("-" * 80)
    
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    result = fetch_with_metadata("get_stock_data", ticker, start_date, end_date)
    
    if result["success"]:
        print(f"✓ 来源: {result['source']}")
        print(f"✓ 字段: {', '.join(result['fields'])}")
        print(f"✓ 数据:\n{result['data'][:500]}")  # 显示前500字符
    else:
        print(f"✗ 失败: {result.get('error', '未知错误')}")
    
    print()
    
    # 2. 基本面快照
    print("2. 基本面快照")
    print("-" * 80)
    
    result = fetch_with_metadata("get_fundamentals", ticker, end_date)
    
    if result["success"]:
        print(f"✓ 来源: {result['source']}")
        print(f"✓ 字段: {', '.join(result['fields'])}")
        print(f"✓ 数据:\n{result['data']}")
    else:
        print(f"✗ 失败: {result.get('error', '未知错误')}")


def cmd_financial(ticker: str):
    """财务报表：三表"""
    print(f"\n{'='*80}")
    print(f"【财务报表】{ticker}")
    print(f"{'='*80}\n")
    
    curr_date = datetime.now().strftime("%Y-%m-%d")
    
    # 1. 利润表
    print("1. 利润表")
    print("-" * 80)
    result = fetch_with_metadata("get_income_statement", ticker, curr_date)
    if result["success"]:
        print(f"✓ 来源: {result['source']}")
        print(f"✓ 防前视: {result.get('防前视', '?')}")
        print(f"✓ 数据:\n{result['data'][:800]}")
    else:
        print(f"✗ 失败: {result.get('error', '未知错误')}")
    
    print()
    
    # 2. 资产负债表
    print("2. 资产负债表")
    print("-" * 80)
    result = fetch_with_metadata("get_balance_sheet", ticker, curr_date)
    if result["success"]:
        print(f"✓ 来源: {result['source']}")
        print(f"✓ 防前视: {result.get('防前视', '?')}")
        print(f"✓ 数据:\n{result['data'][:800]}")
    else:
        print(f"✗ 失败: {result.get('error', '未知错误')}")
    
    print()
    
    # 3. 现金流量表
    print("3. 现金流量表")
    print("-" * 80)
    result = fetch_with_metadata("get_cashflow", ticker, curr_date)
    if result["success"]:
        print(f"✓ 来源: {result['source']}")
        print(f"✓ 防前视: {result.get('防前视', '?')}")
        print(f"✓ 数据:\n{result['data'][:800]}")
    else:
        print(f"✗ 失败: {result.get('error', '未知错误')}")


def cmd_flow(ticker: str):
    """资金流+龙虎榜"""
    print(f"\n{'='*80}")
    print(f"【资金流与龙虎榜】{ticker}")
    print(f"{'='*80}\n")
    
    curr_date = datetime.now().strftime("%Y-%m-%d")
    
    # 1. 资金流
    print("1. 个股资金流")
    print("-" * 80)
    result = fetch_with_metadata("get_fund_flow", ticker, curr_date)
    if result["success"]:
        print(f"✓ 来源: {result['source']}")
        print(f"✓ 字段: {', '.join(result['fields'])}")
        print(f"⚠️ 窗口限制: {result.get('窗口限制', '?')}")
        print(f"✓ 数据:\n{result['data'][:800]}")
    else:
        print(f"✗ 失败: {result.get('error', '未知错误')}")
    
    print()
    
    # 2. 龙虎榜
    print("2. 龙虎榜")
    print("-" * 80)
    result = fetch_with_metadata("get_dragon_tiger_board", ticker, curr_date)
    if result["success"]:
        print(f"✓ 来源: {result['source']}")
        print(f"✓ 字段: {', '.join(result['fields'])}")
        print(f"✓ 数据:\n{result['data'][:800]}")
    else:
        print(f"✗ 失败: {result.get('error', '未知错误')}")


def cmd_events(ticker: str):
    """事件：解禁+新闻"""
    print(f"\n{'='*80}")
    print(f"【事件与新闻】{ticker}")
    print(f"{'='*80}\n")
    
    curr_date = datetime.now().strftime("%Y-%m-%d")
    
    # 1. 解禁
    print("1. 限售解禁")
    print("-" * 80)
    result = fetch_with_metadata("get_lockup_expiry", ticker, curr_date)
    if result["success"]:
        print(f"✓ 来源: {result['source']}")
        print(f"✓ 字段: {', '.join(result['fields'])}")
        print(f"✓ 数据:\n{result['data'][:800]}")
    else:
        print(f"✗ 失败: {result.get('error', '未知错误')}")
    
    print()
    
    # 2. 新闻
    print("2. 个股新闻")
    print("-" * 80)
    result = fetch_with_metadata("get_news", ticker, curr_date)
    if result["success"]:
        print(f"✓ 来源: {result['source']}")
        print(f"✓ 字段: {', '.join(result['fields'])}")
        print(f"⚠️ {result.get('注意', '')}")
        print(f"✓ 数据:\n{result['data'][:800]}")
    else:
        print(f"✗ 失败: {result.get('error', '未知错误')}")


def cmd_all(ticker: str):
    """完整数据包"""
    cmd_basic(ticker)
    cmd_financial(ticker)
    cmd_flow(ticker)
    cmd_events(ticker)


def cmd_json(ticker: str, output_file: str = None):
    """JSON格式输出（便于程序化调用）"""
    curr_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    results = {
        "ticker": ticker,
        "timestamp": datetime.now().isoformat(),
        "data": {}
    }
    
    # 获取所有数据
    functions = [
        ("stock_data", "get_stock_data", [ticker, start_date, curr_date]),
        ("fundamentals", "get_fundamentals", [ticker, curr_date]),
        ("income_statement", "get_income_statement", [ticker, curr_date]),
        ("balance_sheet", "get_balance_sheet", [ticker, curr_date]),
        ("cashflow", "get_cashflow", [ticker, curr_date]),
        ("fund_flow", "get_fund_flow", [ticker, curr_date]),
        ("dragon_tiger_board", "get_dragon_tiger_board", [ticker, curr_date]),
        ("lockup_expiry", "get_lockup_expiry", [ticker, curr_date]),
        ("news", "get_news", [ticker, curr_date]),
    ]
    
    for key, func_name, args in functions:
        results["data"][key] = fetch_with_metadata(func_name, *args)
    
    # 输出
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"✓ 已保存到: {output_file}")
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2))


# ============================================================================
# CLI入口
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="TradingAgents-Astock 数据CLI（无LLM模式）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 基础信息（K线+基本面）
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
        """
    )
    
    parser.add_argument("command", choices=["basic", "financial", "flow", "events", "all", "json"],
                       help="命令类型")
    parser.add_argument("ticker", help="6位股票代码（如 300308）")
    parser.add_argument("-o", "--output", help="JSON输出文件路径")
    
    args = parser.parse_args()
    
    # 执行命令
    if args.command == "basic":
        cmd_basic(args.ticker)
    elif args.command == "financial":
        cmd_financial(args.ticker)
    elif args.command == "flow":
        cmd_flow(args.ticker)
    elif args.command == "events":
        cmd_events(args.ticker)
    elif args.command == "all":
        cmd_all(args.ticker)
    elif args.command == "json":
        cmd_json(args.ticker, args.output)


if __name__ == "__main__":
    main()
