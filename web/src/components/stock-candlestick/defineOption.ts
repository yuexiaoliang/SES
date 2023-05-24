import { StockHistory } from "@/apis/typings";
import { EChartsOption, SeriesOption } from "echarts";

export default (data: StockHistory[]) => {
  // K 线数据
  const candlestickData = data.map((item: any) => {
    const { closing, opening, lowest, highest } = item;
    return [opening, closing, lowest, highest];
  });

  const coefficient = Math.max(...candlestickData.map((item: any) => item[1]));

  const items = [
    ["换手率", "turnover_rate", getMax(data, "turnover_rate")],
    ["跌涨幅", "price_chg_pct", getMax(data, "price_chg_pct")],
    ["振幅", "amplitude", getMax(data, "amplitude")],
  ];

  const source: any[] = [];

  data.forEach((item) => {
    const { closing, opening, lowest, highest, date } = item;
    const option: Record<string, any> = {
      closing,
      opening,
      lowest,
      highest,
      raw: item,
    };

    items.forEach(([cnKey, key, maxVal]) => {
      // option[cnKey] = (item[key] / maxVal) * coefficient;
      option[cnKey] = item[key];
    });

    source.push({
      product: date,
      ...option,
    });
  });

  const legend: EChartsOption["legend"] = {
    data: items.map((item) => item[0]) as string[],
  };
  console.log({ source, legend });

  const series: EChartsOption["series"] = [
    {
      name: "k线",
      type: "candlestick",
      yAxisIndex: 0,
      encode: {
        x: "product",
        y: ["opening", "closing", "highest", "lowest"],
        tooltip: ["opening", "closing", "highest", "lowest"],
      },
      itemStyle: {
        color: "#ec0000",
        color0: "#00da3c",
        borderColor: "#8A0000",
        borderColor0: "#008F28",
      },
      // markLine: {
      //   symbol: ["none", "none"],
      //   data: [
      //     {
      //       name: "min line on close",
      //       type: "min",
      //       valueDim: "closing",
      //     },
      //     {
      //       name: "max line on close",
      //       type: "max",
      //       valueDim: "closing",
      //     },
      //   ],
      // },
    },
    ...items.map((item) => {
      const [name] = item;
      return {
        name: name,
        type: "line",
        yAxisIndex: 1,
        encode: {
          x: "product",
          y: name,
        },
        showSymbol: true,
        symbol(data) {
          return data.raw?.label ? "circle" : "none";
        },
        symbolSize: 5,
        lineStyle: {
          width: 1,
        },
      } as SeriesOption;
    }),
  ];

  return {
    title: {
      text: data[0].name,
      left: 0,
    },
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "cross",
      },
      formatter: (params: any) => {
        const { data } = params[0];
        const { date, opening, closing, highest, lowest } = data.raw;
        let result = `
          ${date}<br/>
          开 ${opening} 收 ${closing} 高 ${highest} 低 ${lowest}<br/>
        `;

        items.forEach(([cnKey, key]) => {
          result += `${cnKey}：${data.raw[key]}<br/>`;
        });

        return result;
      },
    },
    legend,
    dataset: {
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

    series,
  } as EChartsOption;
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
