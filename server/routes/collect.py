from fastapi import APIRouter

import collector

from models.stock import NotDataResponse

router = APIRouter()


@router.post("/realtime_stocks", name="采集沪深市场 A 股最新状况", response_model=NotDataResponse)
def collect_realtime_stocks():
    collector.collector.collect_realtime_stocks()
    return {"message": "采集成功", "code": 0, "data": None}


@router.post("/stocks", name="采集沪深市场 A 股信息", response_model=NotDataResponse)
def collect_stocks_base_info():
    collector.collector.collect_stocks()
    return {"message": "采集成功", "code": 0, "data": None}


@router.post("/stocks_history", name="采集沪深市场 A 股日线数据", response_model=NotDataResponse)
def collect_stocks_history():
    collector.collector.collect_stocks_history()
    return {"message": "采集成功", "code": 0, "data": None}


@router.post("/all", name="采集沪深市场 A 股数据", response_model=NotDataResponse)
def collect_all():
    collector.collector.start()
    return {"message": "采集成功", "code": 0, "data": None}
