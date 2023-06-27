
from typing import List, Union
from typing_extensions import Literal
from pydantic import BaseModel, Field
from models.common import ResponseBaseModel
from models.stock import  StockHistory

class StockSimulatedTradingRecord(BaseModel):
    """股票模拟交易的记录"""
    type: Union[Literal["buy"], Literal["sell"]] = Field(..., title='交易类型')
    date: str = Field(..., title='时间')
    price: float = Field(..., title='单价')
    count: int = Field(..., title='数量')
    total: float = Field(..., title='总金额')
    balance: float = Field(..., title='剩余资金')


class StockSimulatedTrading(BaseModel):
    """股票模拟交易"""
    stock_code: str = Field(..., title='股票代码')
    status: Union[Literal["long"], Literal["short"]] = Field(..., title='状态：long-持仓 short-空仓')
    holdings: int = Field(..., title='持仓数量')
    balance: float = Field(..., title='剩余资金')
    raw_funds: float = Field(..., title='初始资金')
    market_value: float = Field(..., title='市值')
    total_funds: float = Field(..., title='总资产')
    holding_time: int = Field(..., title='持仓时间')
    intraday_holding_time: int = Field(..., title='盘中持仓时间')
    records: List[StockSimulatedTradingRecord] = Field(..., title='交易记录')

class SingleStockResponse(ResponseBaseModel):
    class config:
        title = "单只股票交易测试 Response"

    # data: StocksTestResponseData = Field(..., title='返回的数据')
    data: StockSimulatedTrading = Field(..., title='返回的数据')

class MultiStocksResponse(ResponseBaseModel):
    class config:
        title = "多只股票交易测试 Response"

    # data: StocksTestResponseData = Field(..., title='返回的数据')
    data: List[StockSimulatedTrading] = Field(..., title='返回的数据')