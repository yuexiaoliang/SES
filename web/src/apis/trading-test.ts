import http from "@/utils/http";
import { StockHistory } from "./typings";

// 单只股票模拟炒股测试
// 请求参数
export interface GetTradingTestRequestParams {
  end_date?: string;
  raw_funds?: number;
  start_date?: string;
}

/**
 * 返回的数据
 *
 * StockTestResponseData
 */
export interface StockTestResponseData {
  /**
   * 初始资金
   */
  raw_funds: number;
  /**
   * 交易记录
   */
  records: StockTestRecord[];
}

/**
 * StockTestRecord
 */
export interface StockTestRecord {
  /**
   * 买入记录
   */
  buy: Buy;
  /**
   * 卖出记录
   */
  sell?: Sell;
}

/**
 * 买入记录
 *
 * StockTestBuyRecord
 */
export interface Buy {
  /**
   * 可用资金
   */
  available_funds: number;
  /**
   * 买入成本
   */
  cost: number;
  /**
   * 时间
   */
  date: string;
  /**
   * 买入数量
   */
  holdings: number;
  /**
   * 买入单价
   */
  price: number;
  /**
   * 本金
   */
  principal: number;
  /**
   * 总金额
   */
  total: number;

  /**
   * 当天交易数据
   */
  raw: StockHistory;
}

/**
 * 卖出记录
 *
 * StockTestSellRecord
 */
export interface Sell {
  /**
   * 可用资金
   */
  available_funds: number;
  /**
   * 时间
   */
  date: string;
  /**
   * 收益率
   */
  gain_ratio: number;
  /**
   * 持仓时间
   */
  holding_time: number;
  /**
   * 卖出数量
   */
  holdings: number;
  /**
   * 盘中持仓时间
   */
  intraday_holding_time: number;
  /**
   * 卖出单价
   */
  price: number;
  /**
   * 利润
   */
  profit: number;
  /**
   * 总金额
   */
  total: number;

  /**
   * 当天交易数据
   */
  raw: StockHistory;
}

export function getTradingTest(
  code: string,
  params: GetTradingTestRequestParams
) {
  return http.get<StockTestResponseData>(`/trading_test/single/${code}`, {
    params,
  });
}

export interface GetTradingTestStocksParams {
  end_date?: string;
  raw_funds?: number;
  start_date?: string;
  stocks: string;
}
export function getTradingTestStocks(params: GetTradingTestStocksParams) {
  return http.get<StockTestResponseData[]>(`/trading_test/stocks`, {
    params
  });
}
