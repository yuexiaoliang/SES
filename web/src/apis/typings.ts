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
   * 流通市值
   */
  circulating_cap?: number;
  /**
   * 股票代码
   */
  code: string;
  /**
   * 动态市盈率
   */
  dynamic_pe?: number;
  /**
   * 毛利率
   */
  gross_margin?: number;
  /**
   * 最高
   */
  highest?: number;
  /**
   * 所属行业
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
  lowest?: number;
  /**
   * 总市值
   */
  market_cap?: number;
  /**
   * 市场类型
   */
  market_type: string;
  /**
   * 股票名称
   */
  name: string;
  /**
   * 净利率
   */
  net_margin?: number;
  /**
   * 净利润
   */
  net_profit?: number;
  /**
   * 今开
   */
  open?: number;
  /**
   * 市净率
   */
  pb_ratio?: number;
  /**
   * 市盈率(动)
   */
  pe_ratio?: number;
  /**
   * 昨日收盘
   */
  prev_close?: number;
  /**
   * 涨跌额
   */
  price_chg_amt?: number;
  /**
   * 涨跌幅
   */
  price_chg_pct?: number;
  /**
   * 行情ID
   */
  quote_id: string;
  /**
   * ROE
   */
  roe?: number;
  /**
   * 板块编号
   */
  sector_id?: string;
  /**
   * 成交额
   */
  turnover?: number;
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
  vol_ratio?: number;
  /**
   * 成交量
   */
  volume?: number;
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
   * 收盘价
   */
  closing: number;
  /**
   * 股票代码
   */
  code: string;
  /**
   * 日期
   */
  date: string;
  /**
   * 最高价
   */
  highest: number;
  /**
   * 唯一标识
   */
  id: string;
  /**
   * 最低价
   */
  lowest: number;
  /**
   * 股票名称
   */
  name: string;
  /**
   * 开盘价
   */
  opening: number;
  /**
   * 涨跌额
   */
  price_chg_amt: number;
  /**
   * 涨跌幅
   */
  price_chg_pct: number;
  /**
   * 成交额
   */
  turnover: number;
  /**
   * 换手率
   */
  turnover_rate: number;
  /**
   * 成交量
   */
  volume: number;
}

export interface GetStockByCodePathParams {
  code: string;
}

export interface GetStockDailyDataParams {
  code: string;
  end_date?: string;
  start_date?: string;
}
