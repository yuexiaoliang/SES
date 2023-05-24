// @ts-nocheck
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

export function filterDataByPriceChange(data, threshold, dateRange, label) {
  const filteredData = [];
  const filteredDataMap = {};

  for (let i = 1; i < data.length; i++) {
    const prevData = data[i - 1];
    const currentData = data[i];

    if (data[i].price_chg_pct > threshold) {
      const labeledData = { ...currentData, label };
      const labeledDataKey = `${labeledData.code}_${labeledData.date}`;

      if (!filteredDataMap[labeledDataKey]) {
        filteredData.push(labeledData);
        filteredDataMap[labeledDataKey] = true;
      }

      for (let j = 1; j <= dateRange; j++) {
        const prevIndex = i - j;
        const nextIndex = i + j;

        if (prevIndex >= 0) {
          const prevRelatedData = data[prevIndex];
          const prevRelatedDataKey = `${prevRelatedData.code}_${prevRelatedData.date}`;
          if (!filteredDataMap[prevRelatedDataKey]) {
            filteredData.push(prevRelatedData);
            filteredDataMap[prevRelatedDataKey] = true;
          }
        }

        if (nextIndex < data.length) {
          const nextRelatedData = data[nextIndex];
          const nextRelatedDataKey = `${nextRelatedData.code}_${nextRelatedData.date}`;
          if (!filteredDataMap[nextRelatedDataKey]) {
            filteredData.push(nextRelatedData);
            filteredDataMap[nextRelatedDataKey] = true;
          }
        }
      }
    }
  }

  // Sort filteredData by date
  filteredData.sort((a, b) => {
    if (a.date < b.date) {
      return -1;
    } else if (a.date > b.date) {
      return 1;
    } else {
      return 0;
    }
  });

  return filteredData;
}
