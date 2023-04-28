from enum import Enum

class CollectedType(Enum):
  REALTIME_STOCKS = "realtime_stocks"
  STOCKS_BASE_INFO = "stocks_base_info"
  STOCKS_HISTORY = "stocks_history"

column_mapping = {
  "股票代码": "code",
  "股票名称": "name",
  "涨跌幅": "chg_pct",
  "最新价": "latest_price",
  "最高": "highest",
  "最低": "lowest",
  "今开": "open",
  "涨跌额": "chg_amt",
  "换手率": "turnover_rate",
  "量比": "vol_ratio",
  "动态市盈率": "dynamic_pe",
  "成交量": "volume",
  "成交额": "turnover",
  "昨日收盘": "prev_close",
  "总市值": "market_cap",
  "流通市值": "circulating_cap",
  "行情ID": "quote_id",
  "市场类型": "market_type",
  "更新时间": "update_time",
  "最新交易日": "latest_trading_day",
  "净利润": "net_profit",
  "所处行业": "industry",
  "市盈率(动)": "pe_ratio",
  "市净率": "pb_ratio",
  "ROE": "roe",
  "毛利率": "gross_margin",
  "净利率": "net_margin",
  "板块编号": "sector_id",
  "日期": "date",
  "开盘": "opening",
  "收盘": "closing",
  "振幅": "amplitude",
  "涨跌幅": "price_chg_pct",
  "涨跌额": "price_chg_amt",
  "换手率": "turnover_rate_1"
}

DEFAULT_START_COLLECT_TIME = '20230428'
