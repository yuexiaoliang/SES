import http from "@/utils/http";
import {
  RequestListCommonParams,
  GetStockByCodePathParams,
  GetStockDailyDataParams,
  Stock,
  StockHistory,
  ResponseListData,
} from "./typings";

// 获取股票列表
export const getStockList = (params: RequestListCommonParams) => {
  return http.get<ResponseListData<Stock[]>>("/stock/list", { params });
};

// 根据股票 Code 获取股票信息
export const getStockByCode = (params: GetStockByCodePathParams) => {
  return http.get<Stock>(`/stock/${params.code}`);
};

// 获取股票日线数据
export const getStockDailyData = (
  code: string,
  params?: GetStockDailyDataParams
) => {
  return http.get<StockHistory[]>(`/stock/daily-data/${code}`, {
    params,
  });
};
