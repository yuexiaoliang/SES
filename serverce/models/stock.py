from pydantic import BaseModel, Field
from typing import List


from .common import ResponseBaseModel, ResponseListModel


class NotDataResponse(ResponseBaseModel):
    data: None


class StockBaseModel(BaseModel):
    id: str = Field(..., title='唯一标识')
    stock_code: str = Field(..., title='股票代码')
    stock_name: str = Field(..., title='股票名称')


class Stock(StockBaseModel):
    class Config:
        title = '股票信息'

    net_profit: float = Field(None, title='净利润')
    total_market_value: float = Field(None, title='总市值')
    circulating_market_value: float = Field(None, title='流通市值')
    industry: str = Field(None, title='所处行业')
    pe_ratio: float = Field(None, title='市盈率(动)')
    pb_ratio: float = Field(None, title='市净率')
    gross_profit_margin: float = Field(None, title='毛利率')
    net_profit_margin: float = Field(None, title='净利率')
    plate_code: str = Field(None, title='板块编号')
    roe: float = Field(None, title='ROE')
    change_percent: float = Field(None, title='涨跌幅')
    latest_price: float = Field(None, title='最新价')
    highest_price: float = Field(None, title='最高')
    lowest_price: float = Field(None, title='最低')
    opening_price: float = Field(None, title='今开')
    change_amount: float = Field(None, title='涨跌额')
    turnover_rate: float = Field(None, title='换手率')
    volume_ratio: float = Field(None, title='量比')
    dynamic_pe_ratio: float = Field(None, title='动态市盈率')
    transaction_volume: int = Field(None, title='成交量')
    transaction_amount: float = Field(None, title='成交额')
    previous_closing_price: float = Field(None, title='昨日收盘')
    quote_id: str = Field(..., title='行情ID')
    market_type: str = Field(..., title='市场类型')
    update_time: str = Field(..., title='更新时间')
    latest_trading_day: str = Field(..., title='最新交易日')


class StockHistory(StockBaseModel):
    class config:
        title = "股票历史信息"

    date: str = Field(..., title='日期')
    amplitude: float = Field(..., title='振幅')
    closing_price: float = Field(..., title='收盘价')
    highest_price: float = Field(..., title='最高价')
    lowest_price: float = Field(..., title='最低价')
    opening_price: float = Field(..., title='开盘价')
    change_amount: float = Field(..., title='涨跌额')
    change_percent: float = Field(..., title='涨跌幅')
    transaction_amount: float = Field(..., title='成交额')
    turnover_rate: float = Field(..., title='换手率')
    transaction_volume: int = Field(..., title='成交量')


class StockHistoryResponse(ResponseBaseModel):
    class config:
        title = "股票历史信息 Response"

    data: List[StockHistory]


class StockResponse(ResponseBaseModel):
    class config:
        title = "股票信息 Response"

    data: Stock


class StocksResponse(ResponseBaseModel):
    class config:
        title = "股票信息列表 Response"

    class StocksInfo(ResponseListModel):
        list: List[Stock]

    data: StocksInfo
