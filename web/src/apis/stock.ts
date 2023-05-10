import http from "@/utils/http";
import {
  RequestListCommonParams,
  GetStockByCodePathParams,
  GetStockDailyDataParams,
  Stock,
  StockHistory,
} from "./typings";

// 获取股票列表
export const getStockList = (params: RequestListCommonParams) => {
  return http.get<Stock[]>("/stock/list", { params });
};

// 根据股票 Code 获取股票信息
export const getStockByCode = (params: GetStockByCodePathParams) => {
  return http.get<Stock>(`/stock/${params.code}`);
};

// 获取股票日线数据
export const getStockDailyData = (params: GetStockDailyDataParams) => {
  return http.get<StockHistory[]>(`/stock/daily-data/${params.code}`);
};
