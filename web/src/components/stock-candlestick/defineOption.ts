import { StockHistory } from "@/apis/typings";

export default (data: StockHistory[]) => {
  const upColor = "#ec0000";
  const upBorderColor = "#8A0000";
  const downColor = "#00da3c";
  const downBorderColor = "#008F28";

  // K 线数据
  const candlestickData = data.map((item: any) => {
    const { closing, opening, lowest, highest } = item;
    return [opening, closing, lowest, highest];
  });

  const coefficient = Math.max(...candlestickData.map((item: any) => item[1]));;

  // X 轴数据
  const xAxisData = data.map((item: any) => {
    const { date } = item;
    return date;
  });

  // 换手率
  const turnoverRate = normalizeData(data, "turnover_rate", coefficient);

  // 振幅
  const amplitude = normalizeData(data, "amplitude", coefficient);

  // 成交量
  const volume = normalizeData(data, "volume", coefficient);

  // 成交额
  const turnover = normalizeData(data, "turnover", coefficient);

  // 跌涨幅
  const priceChgPct = normalizeData(data, "price_chg_pct", coefficient);

  // 跌涨额
  const priceChgAmt = normalizeData(data, "price_chg_amt", coefficient);

  return {
    title: {
      text: "上证指数",
      left: 0,
    },
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "cross",
      },
    },
    legend: {
      data: ["日K", "换手率", "跌涨幅", "跌涨额", "振幅", "成交量", "成交额"],
    },
    grid: {
      left: "10%",
      right: "10%",
      bottom: "15%",
    },
    xAxis: {
      type: "category",
      data: xAxisData,
      boundaryGap: false,
      axisLine: { onZero: false },
      splitLine: { show: false },
      min: "dataMin",
      max: "dataMax",
    },
    yAxis: [
      {
        scale: true,
        splitArea: {
          show: true,
        },
      },
      {
        scale: true,
        splitArea: {
          show: true,
        },
      },
    ],
    dataZoom: [
      {
        type: "inside",
        start: 50,
        end: 100,
      },
      {
        show: true,
        type: "slider",
        top: "90%",
        start: 50,
        end: 100,
      },
    ],
    series: [
      {
        name: "日K",
        type: "candlestick",
        yAxisIndex: 0,
        data: candlestickData,
        itemStyle: {
          color: upColor,
          color0: downColor,
          borderColor: upBorderColor,
          borderColor0: downBorderColor,
        },
        markLine: {
          symbol: ["none", "none"],
          data: [
            {
              name: "min line on close",
              type: "min",
              valueDim: "close",
            },
            {
              name: "max line on close",
              type: "max",
              valueDim: "close",
            },
          ],
        },
      },
      {
        name: "换手率",
        type: "line",
        yAxisIndex: 1,
        data: turnoverRate,
        smooth: true,
        lineStyle: {
          opacity: 0.5,
        },
      },
      {
        name: "振幅",
        type: "line",
        yAxisIndex: 1,
        data: amplitude,
        smooth: true,
        lineStyle: {
          opacity: 0.5,
        },
      },
      {
        name: "成交量",
        type: "line",
        yAxisIndex: 1,
        data: volume,
        smooth: true,
        lineStyle: {
          opacity: 0.5,
        },
      },
      {
        name: "成交额",
        type: "line",
        yAxisIndex: 1,
        data: turnover,
        smooth: true,
        lineStyle: {
          opacity: 0.5,
        },
      },

      {
        name: "跌涨幅",
        type: "line",
        yAxisIndex: 1,
        data: priceChgPct,
        smooth: true,
        lineStyle: {
          opacity: 0.5,
        },
      },
      {
        name: "跌涨额",
        type: "line",
        yAxisIndex: 1,
        data: priceChgAmt,
        smooth: true,
        lineStyle: {
          opacity: 0.5,
        },
      },
    ],
  };
};

function normalizeData(
  data: any[],
  indicator: string,
  coefficient: number
): number[] {
  const indicatorData = data.map((item: any) => {
    return item[indicator];
  });
  const maxIndicator = Math.max(...indicatorData);
  return indicatorData.map((item: any) => {
    return (item / maxIndicator) * coefficient;
  });
}
