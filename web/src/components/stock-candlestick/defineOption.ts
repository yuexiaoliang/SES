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

  const coefficient = Math.max(...candlestickData.map((item: any) => item[1]));

  const items = [
    ["换手率", "turnover_rate", getMax(data, "turnover_rate")],
    ["跌涨幅", "price_chg_pct", getMax(data, "price_chg_pct")],
    ["跌涨额", "price_chg_amt", getMax(data, "price_chg_amt")],
    ["振幅", "amplitude", getMax(data, "amplitude")],
    ["成交量", "volume", getMax(data, "volume")],
    ["成交额", "turnover", getMax(data, "turnover")],
  ];

  const source: any[] = [];
  const dimensions = ["product"].concat(items.map((item) => item[0]));

  data.forEach((item) => {
    const { closing, opening, lowest, highest, date } = item;
    const k = [date, opening, closing, lowest, highest];
    const option: Record<string, any> = { closing, opening, lowest, highest };

    items.forEach(([cnKey, key, maxVal], index) => {
      if (index === 0) {
        option[cnKey] = k;
        return;
      }
      option[cnKey] = (item[key] / maxVal) * coefficient;
    });

    source.push({
      product: date,
      ...option,
    });
  });
  console.log({ dimensions, source });

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
    legend: {},
    dataset: {
      // dimensions,
      source,
    },
    grid: {
      left: "10%",
      right: "10%",
      bottom: "15%",
    },
    xAxis: {
      type: "category",
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
        type: "candlestick",
        yAxisIndex: 0,
        encode: {
          x: "product",
          y: ["opening", "closing", "highest", "lowest"],
        },
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
              valueDim: "closing",
            },
            {
              name: "max line on close",
              type: "max",
              valueDim: "closing",
            },
          ],
        },
      },
      {
        type: "line",
        yAxisIndex: 1,
        smooth: true,
        lineStyle: {
          opacity: 0.5,
        },
      },
      {
        type: "line",
        yAxisIndex: 1,
        smooth: true,
        lineStyle: {
          opacity: 0.5,
        },
      },
      {
        type: "line",
        yAxisIndex: 1,
        smooth: true,
        lineStyle: {
          opacity: 0.5,
        },
      },
      {
        type: "line",
        yAxisIndex: 1,
        smooth: true,
        lineStyle: {
          opacity: 0.5,
        },
      },

      {
        type: "line",
        yAxisIndex: 1,
        smooth: true,
        lineStyle: {
          opacity: 0.5,
        },
      },
      {
        type: "line",
        yAxisIndex: 1,
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

function getMax(data: any[], indicator: string): number[] {
  const indicatorData = data.map((item: any) => {
    return item[indicator];
  });
  return Math.max(...indicatorData);
}
