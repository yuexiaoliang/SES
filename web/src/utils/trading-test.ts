import { StockHistoryWithAny } from "@/apis/typings";
import { StockSimulatedTradingRecord } from "@/apis/trading-test";

export function addBSToData(
  data: StockHistoryWithAny[],
  tradingData: StockSimulatedTradingRecord[]
) {
  tradingData.forEach((record) => {
    const { type, date } = record

    if (type === 'buy') {
      const index = data.findIndex((item) => item.date === date);
      data[index].buyRecord = record;
    }

    if (type === 'sell') {
      const index = data.findIndex((item) => item.date === date);
      data[index].sellRecord = record;
    }
  });

  return data
}
