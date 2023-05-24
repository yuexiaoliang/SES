import { StockHistory } from "@/apis/typings";

export function filterDataByPriceChgPctAndDateRange(
  data: StockHistory[],
  priceChgPct: number,
  dateRange: number,
  label: any
): StockHistory[] {
  const filteredData = [];
  const filteredDataMap = {};

  for (let i = 0; i < data.length; i++) {
    const currentData = data[i];
    const currentPriceChgPct = currentData.price_chg_pct;
    const currentDate = new Date(currentData.date);
    const startDate = new Date(
      currentDate.getTime() - dateRange * 24 * 60 * 60 * 1000
    );
    const endDate = new Date(
      currentDate.getTime() + dateRange * 24 * 60 * 60 * 1000
    );
    const startDateStr = startDate.toISOString().slice(0, 10);
    const endDateStr = endDate.toISOString().slice(0, 10);

    if (
      currentPriceChgPct > priceChgPct &&
      currentData.date >= startDateStr &&
      currentData.date <= endDateStr
    ) {
      const labeledData = { ...currentData, label };
      const labeledDataKey = `${labeledData.code}_${labeledData.date}`;

      if (!filteredDataMap[labeledDataKey]) {
        filteredData.push(labeledData);
        filteredDataMap[labeledDataKey] = true;
      }

      const relatedData = data.filter(
        (d) =>
          d.code === currentData.code &&
          d.date >= startDateStr &&
          d.date <= endDateStr
      );

      relatedData.forEach((d) => {
        const relatedDataKey = `${d.code}_${d.date}`;
        if (!filteredDataMap[relatedDataKey]) {
          filteredData.push(d);
          filteredDataMap[relatedDataKey] = true;
        }
      });
    }
  }

  return filteredData;
}
