from fastapi import FastAPI
from .stock import router as stock
from .collect import router as collect

app = FastAPI()

app.include_router(stock, prefix='/stock', tags=['stock'])
app.include_router(collect, prefix='/collect', tags=['collect'])
