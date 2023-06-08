// import { StockHistory } from "@/apis/typings";

/**
 * 股票历史信息
 */
interface StockHistory {
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
type MACD = number[];
type EMA = number[];
type DIF = number[];
type DEA = number[];
type MA = (number | null)[];

// 计算 EMA
export function calculateEMA(data: StockHistory[], period: number) {
  let result: EMA = [];

  if (data.length < 2) return result;

  let k = 2 / (period + 1);

  let prev = data[0].closing_price; // 初始EMA值为第一个收盘价

  result.push(prev);

  for (let i = 1; i < data.length; i++) {
    let close = data[i].closing_price;

    let curr = k * (close - prev) + prev;

    result.push(curr);

    prev = curr;
  }

  return result;
}

// 计算 DIF
export function calculateDIFFromEMA(emaShort: EMA, emaLong: EMA) {
  let dif: DIF = [];

  for (let i = 0; i < emaShort.length; i++) {
    dif.push(emaShort[i] - emaLong[i]);
  }

  return dif;
}

// 计算 DEA
export function calculateDEA(dif: DIF, n = 9) {
  let emaDif: DIF = [];
  let dea: DEA = [];

  for (let i = 0; i < dif.length; i++) {
    if (i === 0) {
      emaDif.push(dif[i]);
      dea.push(dif[i]);
    } else {
      emaDif.push((2 * dif[i] + (n - 1) * emaDif[i - 1]) / (n + 1));
      dea.push((2 * emaDif[i] + (n - 1) * dea[i - 1]) / (n + 1));
    }
  }

  return dea;
}

// 计算 MACD
export function calculateMACD(dif: DIF, dea: DEA) {
  let macd: MACD = [];

  for (let i = 0; i < dif.length; i++) {
    macd.push((dif[i] - dea[i]) * 2);
  }

  return macd;
}

// 计算 MA
export function calculateMA(data: StockHistory[], dayCount: number) {
  let result: MA = [];

  for (let i = 0, len = data.length; i < len; i++) {
    if (i < dayCount - 1) {
      result.push(null);
      continue;
    }

    let sum = 0;
    for (let j = 0; j < dayCount; j++) {
      sum += data[i - j].closing_price;
    }
    result.push(Number((sum / dayCount).toFixed(2)));
  }

  return result;
}
