## 采集日 K 数据

采集所有股票日 K 数据，并计算振幅入库 - 最后采集日期（默认 2008）年至今，每日 15:10 分采集，并保存最后采集日期。

## 采集股票基本信息

每日 8:50 采集

## 交易逻辑

- 实时获取以持仓股票分 K 数据，自动计算、设置止损点

- 获取股票最新交易日成交明细
  实时成交信息

- 获取沪深市场股票最新行情快照
  用来展示股票最新交易的基本信息

- 获取单只股票最新交易日的日内分钟级单子流入流出数据
  可用来辅助判断价格波动

- 获取沪深市场指定股票前十大股东信息
  可用来辅助判断异动情况

## 可踩数据以及接口

```python
# 获取沪深市场多只股票的实时涨幅情况
# efinance.stock.get_latest_quote(stock_codes: Union[str, List[str]], **kwargs) → DataFrame

# 获取股票的 K 线数据
# efinance.stock.get_quote_history(stock_codes: Union[str, List[str]], beg: str = '19000101', end: str = '20500101', klt: int = 101, fqt: int = 1, **kwargs) → Union[DataFrame, Dict[str, DataFrame]]

# 获取股票基本信息
# efinance.stock.get_base_info(stock_codes: Union[str, List[str]]) → Union[Series, DataFrame]

# 获取股票最新交易日成交明细
# efinance.stock.get_deal_detail(stock_code: str, max_count: int = 1000000, **kwargs) → DataFrame

# 获取沪深市场股票最新行情快照
# efinance.stock.get_quote_snapshot(stock_code: str) → Series

# 获取股票所属板块
# efinance.stock.get_belong_board(stock_code: str) → DataFrame

# 获取企业 IPO 审核状态
# efinance.stock.get_latest_ipo_info() → DataFrame

# 获取单只股票历史单子流入流出数据
# efinance.stock.get_history_bill(stock_code: str) → DataFrame

# 获取单只股票最新交易日的日内分钟级单子流入流出数据
# efinance.stock.get_today_bill(stock_code: str) → DataFrame

# 获取沪深A股市场最新公开的股东数目变化情况 也可获取指定报告期的股东数目变化情况
# efinance.stock.get_latest_holder_number(date: str = None) → DataFrame

# 获取沪深市场指定股票前十大股东信息
# efinance.stock.get_top10_stock_holder_info(stock_code: str, top: int = 4) → DataFrame

# ---------------
# 获取沪深市场的全部股票报告期信息
# efinance.stock.get_all_report_dates() → DataFrame


# 获取龙虎榜详情数据
# efinance.stock.get_daily_billboard(start_date: str = None, end_date: str = None) → DataFrame

# 获取指数成分股信息
# efinance.stock.get_members(index_code: str) → DataFrame

# 获取沪深市场股票某一季度的表现情况
# efinance.stock.get_all_company_performance(date: str = None) → DataFrame

# 获取单个或者多个市场行情的最新状况
# efinance.stock.get_realtime_quotes(fs: Union[str, List[str]] = None, **kwargs) → DataFrame
```
