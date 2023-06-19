import { StockHistoryWithAny } from "@/apis/typings";
import { StockTestRecord } from "@/apis/trading-test";

export function addBSToData(
  data: StockHistoryWithAny[],
  tradingData: StockTestRecord[]
) {
  tradingData.forEach((record) => {
    const { buy, sell } = record;

    if (buy) {
      const { date } = buy;
      const index = data.findIndex((item) => item.date === date);
      data[index].buyRecord = buy;
    }

    if (sell) {
      const { date } = sell;
      const index = data.findIndex((item) => item.date === date);
      data[index].sellRecord = sell;
    }
  });

  return data
}
