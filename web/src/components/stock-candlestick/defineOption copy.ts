import { StockHistory } from "@/apis/typings";
import { convertMAFields } from "@/utils/data-tools";
import { EChartsOption, SeriesOption } from "echarts";

export default (data: StockHistory[]) => {
  // K 线数据
  const candlestickData = data.map((item: any) => {
    const { closing_price, opening_price, lowest_price, highest_price } = item;
    return [opening_price, closing_price, lowest_price, highest_price];
  });

  const coefficient = Math.max(...candlestickData.map((item: any) => item[1]));

  const items = [
    // ["换手率", "turnover_rate", getMax(data, "turnover_rate")],
    // ["跌涨幅", "change_percent", getMax(data, "change_percent")],
    // ["跌涨幅", "change_percent"],
    // ["振幅", "amplitude", getMax(data, "amplitude")],
  ];

  const maItems = convertMAFields(data);

  const source: any[] = [];

  data.forEach((item) => {
    const { closing_price, opening_price, lowest_price, highest_price, date } =
      item;
    const option: Record<string, any> = {
      closing_price,
      opening_price,
      lowest_price,
      highest_price,
      raw: item,
    };

    items.forEach(([cnKey, key, maxVal]) => {
      // option[cnKey] = (item[key] / maxVal) * coefficient;
      option[cnKey] = item[key];
    });

    maItems.forEach(([cnKey, key]) => {
      option[cnKey] = item[key];
    });

    source.push({
      product: date,
      ...option,
    });
  });

  const legend: EChartsOption["legend"] = {
    data: (items.map((item) => item[0]) as string[]).concat(
      maItems.map((item) => item[0]) as string[]
    ),
  };

  const series: EChartsOption["series"] = [
    {
      name: "k线",
      type: "candlestick",
      yAxisIndex: 0,
      encode: {
        x: "product",
        y: ["opening_price", "closing_price", "highest_price", "lowest_price"],
        tooltip: [
          "opening_price",
          "closing_price",
          "highest_price",
          "lowest_price",
        ],
      },
      itemStyle: {
        color: "#ec0000",
        color0: "#00da3c",
        borderColor: "#8A0000",
        borderColor0: "#008F28",
      },
      markPoint: {
        // data: [
        //   {
        //     name: "Mark",
        //     coord: ["2013/5/30", 2200],
        //     value: 2100,
        //   },
        // ],
        data: data.filter(item => item.raise).map(item => {
          return {
            name: "Mark",
            coord: [item.date, item.closing_price],
            value: item.raise,
          }
        })
      },
      // markLine: {
      //   symbol: ["none", "none"],
      //   data: [
      //     {
      //       name: "min line on close",
      //       type: "min",
      //       valueDim: "closing_price",
      //     },
      //     {
      //       name: "max line on close",
      //       type: "max",
      //       valueDim: "closing_price",
      //     },
      //   ],
      // },
    },
    ...maItems.map((item) => {
      const [name] = item;
      return {
        name: name,
        type: "line",
        yAxisIndex: 0,
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
      text: data[0].stock_name,
      left: 0,
    },
    tooltip: {
      trigger: "axis",
      axisPointer: {
        type: "cross",
      },
      formatter: (params: any) => {
        const { data } = params[0];
        const {
          date,
          opening_price,
          closing_price,
          highest_price,
          lowest_price,
        } = data.raw;
        let result = `
          ${date}<br/>
          开 ${opening_price} 收 ${closing_price} 高 ${highest_price} 低 ${lowest_price}<br/>
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
