from fastapi import FastAPI
from .stock import router as stock
from .collect import router as collect
from .trading_test import router as trading_test

app = FastAPI()
app.include_router(stock, prefix='/stock', tags=['stock'])
app.include_router(collect, prefix='/collect', tags=['collect'])
app.include_router(trading_test, prefix='/trading_test', tags=['trading_test'])