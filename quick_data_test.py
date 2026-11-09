#!/usr/bin/env python3
"""
快速数据测试 - 仅HTTP源（避免mootdx连接超时）
"""

import sys
sys.path.insert(0, '/workspace')

from datetime import datetime
from tradingagents.dataflows import a_stock

def test_http_sources(ticker):
    """测试纯HTTP源（快速）"""
    print(f"\n{'='*80}")
    print(f"快速数据测试: {ticker}")
    print(f"{'='*80}\n")
    
    curr_date = datetime.now().strftime("%Y-%m-%d")
    
    # 1. 基本面（腾讯）
    print("1. 基本面快照（腾讯财经）")
    print("-" * 80)
    try:
        data = a_stock.get_fundamentals(ticker, curr_date)
        print(f"✓ 成功")
        print(f"数据:\n{data}\n")
    except Exception as e:
        print(f"✗ 失败: {e}\n")
    
    # 2. 利润表（新浪）
    print("2. 利润表（新浪财报，防前视）")
    print("-" * 80)
    try:
        data = a_stock.get_income_statement(ticker, curr_date)
        print(f"✓ 成功")
        print(f"数据（前500字符）:\n{data[:500]}\n")
    except Exception as e:
        print(f"✗ 失败: {e}\n")
    
    # 3. 资金流（东财）
    print("3. 资金流（东财push2his，注意窗口限制）")
    print("-" * 80)
    try:
        data = a_stock.get_fund_flow(ticker, curr_date)
        print(f"✓ 成功")
        print(f"数据（前500字符）:\n{data[:500]}\n")
    except Exception as e:
        print(f"✗ 失败: {e}\n")
    
    # 4. 龙虎榜（东财）
    print("4. 龙虎榜（东财datacenter）")
    print("-" * 80)
    try:
        data = a_stock.get_dragon_tiger_board(ticker, curr_date)
        print(f"✓ 成功")
        print(f"数据（前500字符）:\n{data[:500]}\n")
    except Exception as e:
        print(f"✗ 失败: {e}\n")
    
    # 5. 解禁（东财）
    print("5. 限售解禁（东财datacenter）")
    print("-" * 80)
    try:
        data = a_stock.get_lockup_expiry(ticker, curr_date)
        print(f"✓ 成功")
        print(f"数据（前500字符）:\n{data[:500]}\n")
    except Exception as e:
        print(f"✗ 失败: {e}\n")
    
    # 6. 新闻（东财）
    print("6. 个股新闻（东财，仅文本）")
    print("-" * 80)
    try:
        data = a_stock.get_news(ticker, curr_date)
        print(f"✓ 成功")
        print(f"数据（前500字符）:\n{data[:500]}\n")
    except Exception as e:
        print(f"✗ 失败: {e}\n")

if __name__ == "__main__":
    import sys
    
    tickers = sys.argv[1:] if len(sys.argv) > 1 else ["300308", "300394"]
    
    for ticker in tickers:
        test_http_sources(ticker)
        print("\n" + "="*80 + "\n")
