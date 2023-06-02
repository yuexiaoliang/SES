export interface RequestListCommonParams {
  page_current?: number;
  page_size?: number;
}

export interface Response<Data> {
  code: number;
  data: Data;
  message: string;
}

export interface ResponseListData<List> {
  list: List;
  page_current: number;
  page_size: number;
  total: number;
}

/**
 * 股票信息
 */
export interface Stock {
  /**
   * 涨跌额
   */
  change_amount?: number;
  /**
   * 涨跌幅
   */
  change_percent?: number;
  /**
   * 流通市值
   */
  circulating_market_value?: number;
  /**
   * 动态市盈率
   */
  dynamic_pe_ratio?: number;
  /**
   * 毛利率
   */
  gross_profit_margin?: number;
  /**
   * 最高
   */
  highest_price?: number;
  /**
   * 唯一标识
   */
  id: string;
  /**
   * 所处行业
   */
  industry?: string;
  /**
   * 最新价
   */
  latest_price?: number;
  /**
   * 最新交易日
   */
  latest_trading_day: string;
  /**
   * 最低
   */
  lowest_price?: number;
  /**
   * 市场类型
   */
  market_type: string;
  /**
   * 净利润
   */
  net_profit?: number;
  /**
   * 净利率
   */
  net_profit_margin?: number;
  /**
   * 今开
   */
  opening_price?: number;
  /**
   * 市净率
   */
  pb_ratio?: number;
  /**
   * 市盈率(动)
   */
  pe_ratio?: number;
  /**
   * 板块编号
   */
  plate_code?: string;
  /**
   * 昨日收盘
   */
  previous_closing_price?: number;
  /**
   * 行情ID
   */
  quote_id: string;
  /**
   * ROE
   */
  roe?: number;
  /**
   * 股票代码
   */
  stock_code: string;
  /**
   * 股票名称
   */
  stock_name: string;
  /**
   * 总市值
   */
  total_market_value?: number;
  /**
   * 成交额
   */
  transaction_amount?: number;
  /**
   * 成交量
   */
  transaction_volume?: number;
  /**
   * 换手率
   */
  turnover_rate?: number;
  /**
   * 更新时间
   */
  update_time: string;
  /**
   * 量比
   */
  volume_ratio?: number;
}

/**
 * 股票历史信息
 */
export interface StockHistory {
  /**
   * 振幅
   */
  amplitude: number;
  /**
   * 涨跌额
   */
  change_amount: number;
  /**
   * 涨跌幅
   */
  change_percent: number;
  /**
   * 收盘价
   */
  closing_price: number;
  /**
   * 日期
   */
  date: string;
  /**
   * 最高价
   */
  highest_price: number;
  /**
   * 唯一标识
   */
  id: string;
  /**
   * 最低价
   */
  lowest_price: number;
  /**
   * 开盘价
   */
  opening_price: number;
  /**
   * 股票代码
   */
  stock_code: string;
  /**
   * 股票名称
   */
  stock_name: string;
  /**
   * 成交额
   */
  transaction_amount: number;
  /**
   * 成交量
   */
  transaction_volume: number;
  /**
   * 换手率
   */
  turnover_rate: number;
}

export interface GetStockByCodePathParams {
  code: string;
}

export interface GetStockDailyDataParams {
  end_date?: string;
  start_date?: string;
}
