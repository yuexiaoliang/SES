import Big from "big.js";

import { StockHistory, StockHistoryWithAny } from "@/apis/typings";

// 向对象中添加移动平均线
export function addMAToData(
  data: StockHistory[],
  thresholds: number | number[]
): StockHistoryWithAny[] {
  // 获取收盘价数组
  const closingPrices = data.map((d) => d.closing_price);

  return data.map((item, i) => {
    const result: StockHistoryWithAny = { ...item };

    if (typeof thresholds === "number") {
      calc(thresholds, i, result);
    }

    if (Array.isArray(thresholds)) {
      thresholds.forEach((threshold) => {
        calc(threshold, i, result);
      });
    }

    return result;
  });

  // 计算平均值
  function calc(threshold: number, i: number, result: StockHistoryWithAny) {
    const maKey = `ma_${threshold}`;

    if (i < threshold - 1) {
      result[maKey] = null;
    } else {
      let sum = 0;
      for (let j = i; j >= i - threshold + 1; j--) {
        sum += closingPrices[j];
      }
      const a = new Big(sum);
      const b = new Big(threshold);
      const c = a.div(b);
      result[maKey] = Number(c.toFixed(3));
    }
  }
}

//
export function convertMAFields(data: StockHistoryWithAny[]) {
  const result = [];
  for (const key in data[0]) {
    if (key.startsWith("ma_")) {
      result.push([`MA${key.slice(3)}`, key]);
    }
  }
  return result;
}

export function convertUPFields(
  data: StockHistoryWithAny[],
  percent: number = 5
) {
  return data.map((curr, i) => {
    if (i === 0) return curr;

    const { change_percent } = curr;

    if (change_percent > percent) {
      curr.raise = change_percent;
    }

    return curr;
  });
}
