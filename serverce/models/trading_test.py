
from typing import List
from pydantic import BaseModel, Field
from pydantic import BaseModel
from models.common import ResponseBaseModel
from models.stock import  StockHistory


class StockTestBuyRecord(BaseModel):
    date: str = Field(..., title='时间')
    price: float = Field(..., title='买入单价')
    cost: float = Field(..., title='买入成本')
    holdings: int = Field(..., title='买入数量')
    total: float = Field(..., title='总金额')
    available_funds:float= Field(..., title='可用资金')
    principal: float = Field(..., title='本金')
    raw: StockHistory = Field(..., title='当天交易数据')


class StockTestSellRecord(BaseModel):
    date: str = Field(..., title='时间')
    price: float = Field(..., title='卖出单价')
    holdings: int = Field(..., title='卖出数量')
    total: float = Field(..., title='总金额')
    available_funds: float = Field(..., title='可用资金')
    profit: float = Field(..., title='利润')
    gain_ratio: float = Field(..., title='收益率')
    intraday_holding_time: int = Field(..., title='盘中持仓天数')
    holding_time: int = Field(..., title='持仓天数')
    raw: StockHistory = Field(..., title='当天交易数据')


class StockTestRecord(BaseModel):
    buy: StockTestBuyRecord = Field(..., title='买入记录')
    sell: StockTestSellRecord = Field(None, title='卖出记录')


class StockTestResponseData(BaseModel):
    raw_funds: float = Field(..., title='初始资金')
    records: List[StockTestRecord] = Field(..., title='交易记录')


class StockTestResponse(ResponseBaseModel):
    class config:
        title = "股票交易测试 Response"

    data: StockTestResponseData = Field(..., title='返回的数据')