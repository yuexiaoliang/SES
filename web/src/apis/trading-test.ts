import http from "@/utils/http";

/**
 * 交易类型
 */
export enum Type {
  Buy = "buy",
  Sell = "sell",
}

/**
 * 状态：long-持仓 short-空仓
 */
export enum Status {
  Long = "long",
  Short = "short",
}

/**
 * StockSimulatedTradingRecord
 */
export interface StockSimulatedTradingRecord {
  /**
   * 剩余资金
   */
  balance: number;
  /**
   * 数量
   */
  count: number;
  /**
   * 时间
   */
  date: string;
  /**
   * 单价
   */
  price: number;
  /**
   * 总金额
   */
  total: number;
  /**
   * 交易类型
   */
  type: Type;
}

/**
 * 返回的数据
 *
 * StockSimulatedTrading
 */
export interface StockSimulatedTrading {
  /**
   * 剩余资金
   */
  balance: number;
  /**
   * 持仓数量
   */
  holdings: number;
  /**
   * 盘中持仓时间
   */
  intraday_holding_time: number;
  /**
   * 市值
   */
  market_value: number;
  /**
   * 初始资金
   */
  raw_funds: number;
  /**
   * 交易记录
   */
  records: StockSimulatedTradingRecord[];
  /**
   * 状态：long-持仓 short-空仓
   */
  status: Status;
  /**
   * 股票代码
   */
  stock_code: string;
  /**
   * 总资产
   */
  total_funds: number;
}

export interface GetTradingTestSingleRequest {
  end_date?: string;
  raw_funds?: number;
  start_date?: string;
}

export interface GetTradingTestMultiRequest {
  /**
   * 股票代码列表
   */
  codes: string[];
  /**
   * 结束日期
   */
  end_date?: string;
  /**
   * 初始资金
   */
  raw_funds: number;
  /**
   * 开始日期
   */
  start_date?: string;
}

// 单只股票模拟炒股测试
export const getTradingTestSingle = (
  code: string,
  params: GetTradingTestSingleRequest
) =>
  http.get<StockSimulatedTrading>(`/trading_test/single/${code}`, { params });

// 多只股票模拟炒股测试
export const getTradingTestMulti = (data: GetTradingTestMultiRequest) =>
  http.post<StockSimulatedTrading[]>("/trading_test/multi", data);
