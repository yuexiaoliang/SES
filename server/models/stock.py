from pydantic import BaseModel
from typing import List


from .common import ResponseBaseModel, ResponseListModel


class NotDataResponse(ResponseBaseModel):
    data: None


class Stock(BaseModel):
    _id: str  # 唯一标识
    code: str  # 股票代码
    name: str  # 股票名称
    net_profit: str  # 净利润
    market_cap: str  # 总市值
    circulating_cap: str  # 流通市值
    industry: str  # 所处行业
    pe_ratio: str  # 市盈率(动)
    pb_ratio: str  # 市净率
    gross_margin: str  # 毛利率
    net_margin: str  # 净利率
    sector_id: str  # 板块编号
    roe: str  # ROE
    price_chg_pct: str  # 涨跌幅
    latest_price: str  # 最新价
    highest: str  # 最高
    lowest: str  # 最低
    open: str  # 今开
    price_chg_amt: str  # 涨跌额
    turnover_rate: str  # 换手率
    vol_ratio: str  # 量比
    dynamic_pe: str  # 动态市盈率
    volume: str  # 成交量
    turnover: str  # 成交额
    prev_close: str  # 昨日收盘
    quote_id: str  # 行情ID
    market_type: str  # 市场类型
    update_time: str  # 更新时间
    latest_trading_day: str  # 最新交易日


class StockResponse(ResponseBaseModel):
    data: Stock


class StocksResponse(ResponseBaseModel):
    class StocksInfo(ResponseListModel):
        list: List[Stock]

    data: StocksInfo
