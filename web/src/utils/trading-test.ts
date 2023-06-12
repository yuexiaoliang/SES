import dayjs from "dayjs";
import { formatNumber } from "@/utils/formatter";
import { Stock, StockHistory, StockHistoryWithAny } from "@/apis/typings";

interface BuyRecord {
  history: StockHistory;

  // 时间
  date: string;

  // 买入单价
  price: number;

  // 买入成本
  cost: number;

  // 买入数量
  holdings: number;

  // 总金额
  total: number;

  // 可用资金
  availableFunds: number;

  // 本金
  principal: number;

  // 交易类型
  type: "买入";
}

interface SellRecord {
  history: StockHistory;

  // 时间
  date: string;

  // 卖出单价
  price: number;

  // 卖出数量
  holdings: number;

  // 总金额
  total: number;

  // 可用资金
  availableFunds: number;

  // 本金
  principal: number;

  // 利润
  profit: number;

  // 收益率
  gainRatio: number;

  // 交易类型
  type: "卖出";

  // 持仓时间
  holdingTime: number;
}

export interface TradingRecord {
  buy: BuyRecord;
  sell?: SellRecord;
}

export const tradingTest = (stock: Stock, data: StockHistoryWithAny[]) => {
  // 本金
  let principal = 7000;

  // 可用资金
  let availableFunds = principal;

  // 持仓数量（股）
  let holdings = 0;

  // 交易记录
  const records: TradingRecord[] = [];

  let status = 0; // 0: 未持仓 1: 持仓中

  data.forEach((item, index) => {
    if (index === 0) return;
    if (status === 0) {
      const record = buy(item, index);
      if (record) {
        records.push({ buy: record });
        item.buyRecord = record;
        return;
      }
    }

    if (status === 1) {
      const sellRecord = sell(item);
      if (!sellRecord) return;
      const record = records[records.length - 1];
      record.sell = sellRecord;
      item.sellRecord = record;
      return;
    }
  });

  return [records, data] as [TradingRecord[], StockHistory[]];

  // 买入
  function buy(item: StockHistory, index: number): BuyRecord | undefined {
    const { dif, dea } = item;
    if (!dif || !dea) return;

    const prevItem = data[index - 1];
    const { dif: prevDif, dea: prevDea } = prevItem;

    if (!prevDif || !prevDea) return;

    // MACD 黄金交叉
    const isGoldenCross = dif > dea && prevDif < prevDea;

    // MACD 零轴之上
    const isAboveZeroAxis = dif > 0 && dea > 0;

    // 买入条件成立
    const isEstablish =
      isGoldenCross && isAboveZeroAxis && item.macd && item.macd > 0;

    if (!isEstablish) return;

    // 买入股票数量（手）
    let _count = Math.floor(availableFunds / (item.closing_price * 100));

    // 总金额
    let total = calculateBuyCost(_count * item.closing_price * 100, stock);

    // 动态计算买入数量以及总额
    while (total > availableFunds) {
      _count -= 1;
      total = calculateBuyCost(_count * item.closing_price * 100, stock);
    }

    // 持仓
    holdings = _count * 100;

    // 买入成本（每股）
    const _cost = formatNumber(total / holdings);

    // 可用资金
    availableFunds = formatNumber(availableFunds - holdings * _cost);

    // 状态变更为持仓中
    status = 1;

    return {
      history: { ...item },

      // 时间
      date: item.date,

      // 买入单价
      price: item.closing_price,

      // 买入成本
      cost: _cost,

      // 买入数量
      holdings,

      // 总金额
      total,

      // 可用资金
      availableFunds,

      // 本金
      principal,

      // 交易类型
      type: "买入",
    };
  }

  // 卖出
  function sell(item: StockHistory): SellRecord | undefined {
    const buyData = records[records.length - 1].buy as BuyRecord;

    const buyPrice = buyData.price;

    // 单价
    const price = item.closing_price;

    // 收益率
    const gainRatio = formatNumber(((price - buyPrice) / buyPrice) * 100);

    // 如果收益率低于 5% 并且 高于 -2% 则继续持有
    if (gainRatio < 3 && gainRatio > -2) return;

    // 持仓时间
    const holdingTime = calculateDays(buyData.date, item.date);

    // 卖出总金额
    const total = calculateSellCost(price, holdings, stock);

    // 可用资金
    availableFunds = formatNumber(availableFunds + total);

    // 利润
    const profit = formatNumber(availableFunds - principal);

    // 本金
    principal = availableFunds;

    // 状态变更为未持仓
    status = 0;

    return {
      // 时间
      date: item.date,

      // 卖出单价
      price,

      // 卖出数量
      holdings,

      // 总金额
      total,

      // 可用资金
      availableFunds,

      // 本金
      principal,

      // 利润
      profit,

      // 收益率
      gainRatio,

      // 交易类型
      type: "卖出",

      // 持仓时间
      holdingTime,

      history: { ...item },
    };
  }
};

// 计算过户费
export function calculateTransferFee(total: number, stock: Stock) {
  return stock.market_type === "沪A" ? formatNumber(total * 0.00002) : 0;
}

// 计算佣金
export function calculateCommission(total: number) {
  const commission = formatNumber(total * 0.0003);
  return commission > 5 ? commission : 5;
}

/**
 * 计算每股股票买入成本
 * @param total 单价
 * @param count 数量
 * @param stock 股票信息
 */
export function calculateBuyCost(total: number, stock: Stock) {
  // 过户费
  const transferFee = calculateTransferFee(total, stock);

  // 佣金
  const commission = calculateCommission(total);

  return formatNumber(transferFee + commission + total);
}

/**
 * 计算卖出价格
 * @param price 单价
 * @param count 数量
 * @param stock 股票信息
 */
export function calculateSellCost(price: number, count: number, stock: Stock) {
  const total = price * count;

  // 计算印花税
  const stampDuty = total * 0.001;

  // 过户费
  const transferFee = calculateTransferFee(total, stock);

  // 佣金
  const commission = calculateCommission(total);

  return formatNumber(total - stampDuty - transferFee - commission);
}

// 计算持仓时间
export function calculateDays(start: string, end: string): number {
  const startDate = dayjs(start);
  const endDate = dayjs(end);
  const diff = endDate.diff(startDate, "day");
  return diff;
}
