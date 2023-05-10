import http from "@/utils/http";

// 采集 A 股最新状况
export const collectRealtimeStocks = () => {
  return http.post("/collect/realtime_stocks");
};

// 采集 A 股信息
export const collectStocks = () => {
  return http.post("/collect/stocks");
};

// 采集 A 股历史日 K 数据
export const collectStocksHistory = () => {
  return http.post("/collect/stocks_history");
}

// 采集 A 股所有数据
export const collectAll = () => {
  return http.post("/collect/all");
}