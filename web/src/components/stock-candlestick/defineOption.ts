import { StockHistory } from "@/apis/typings";
import {
  calculateEMA,
  calculateDEA,
  calculateDIFFromEMA,
  calculateMA,
  calculateMACD,
} from "@/utils/calculators";
import { EChartsOption } from "echarts";

export default (data: StockHistory[]) => {
  const dataZoomStart = 80;
  const dataZoomEnd = 100;

  const left = 20
  const right = 20

  const red = "#FD1050";
  const green = "#0CF49B";

  // K 线数据
  const candlestickData = data.map((item: any) => {
    const { closing_price, opening_price, lowest_price, highest_price } = item;
    return [opening_price, closing_price, lowest_price, highest_price];
  });

  // 成交量
  const volumeData = data.map((item: any) => item.transaction_volume);

  const ema12 = calculateEMA(data, 12);
  const ema26 = calculateEMA(data, 26);
  const dif = calculateDIFFromEMA(ema12, ema26);
  const dea = calculateDEA(dif);
  const macd = calculateMACD(dif, dea);

  // X 轴数据
  const xAxis = data.map((item: any) => item.date);

  return {
    backgroundColor: "#19232d",
    title: {
      text: data[0].stock_name,
      color: "#4a657a",
    },

    tooltip: {
      show: false,
    },

    xAxis: [
      {
        show: true,
        scale: true,
        nameGap: 15,
        gridIndex: 0,
        splitNumber: 5,
        axisLine: {
          lineStyle: {
            color: "#4a657a",
          },
        },
        axisLabel: {
          show: false,
        },
        axisTick: {
          show: false,
        },
        data: xAxis,
        axisPointer: {
          label: {
            show: false,
          },
        }, //主图禁用下标显示
      },
      {
        show: true,
        scale: true,
        nameGap: 15,
        gridIndex: 1,
        splitNumber: 5,
        axisLabel: {
          show: false,
        },
        axisTick: {
          show: false,
        },
        data: xAxis,
        axisPointer: {
          label: {
            show: false,
          },
        }, //附图1禁用下标显示
      },
      {
        show: true,
        scale: true,
        gridIndex: 2,
        splitNumber: 5,
        axisLine: {
          lineStyle: {
            color: "#4a657a",
          },
        },
        axisLabel: {
          textStyle: {
            color: "#4a657a",
          },
        },
        data: xAxis,
      },
    ],

    yAxis: [
      {
        position: "right",
        scale: true,
        gridIndex: 0,
        axisLine: {
          lineStyle: {
            color: "#4a657a",
          },
        },
        axisLabel: {
          width: 180,
          textStyle: {
            color: "#4a657a",
          },
        },
        splitLine: {
          show: true,
          lineStyle: {
            color: "4a657a",
            type: "dashed",
          },
        },
      },
      {
        position: "right",
        gridIndex: 1,
        splitNumber: 2,
        minInterval: 0,
        axisLine: {
          lineStyle: {
            color: "#4a657a",
          },
        },
        axisLabel: {
          textStyle: {
            color: "#4a657a",
          },
        },
        splitLine: {
          show: true,
          lineStyle: {
            color: "4a657a",
            type: "dashed",
          },
        },
      },
      {
        position: "right",
        gridIndex: 2,
        axisLine: {
          lineStyle: {
            color: "#fff",
          },
        },

        axisTick: {
          show: false
        },

        axisLabel: {
          show: false,
        },

        splitLine: {
          show: false,
        },
      },
    ],

    dataZoom: [
      {
        show: false,
        type: "inside",
        start: dataZoomStart,
        end: dataZoomEnd,
        xAxisIndex: [0, 0],
      },
      {
        show: false,
        type: "inside",
        start: dataZoomStart,
        end: dataZoomEnd,
        xAxisIndex: [0, 1],
      },
      {
        show: false,
        type: "inside",
        start: dataZoomStart,
        end: dataZoomEnd,
        xAxisIndex: [0, 2],
      },
      {
        show: false,
      },
    ],

    axisPointer: {
      show: true,
      type: "line",
      link: [
        {
          xAxisIndex: "all",
        },
      ],
    },

    series: [
      {
        type: "candlestick",
        xAxisIndex: 0,
        yAxisIndex: 0,
        data: candlestickData,
        markPoint: {
          symbol: "circle",
          symbolSize: function (_value, param) {
            let size = 15;
            if (param.name === "最高价" || param.name === "最底价") {
              size = 0.1;
            }
            return size;
          },

          label: {
            show: true,
            fontSize: 12,
            color: "#fff",
            formatter(param) {
              const { name, value } = param;

              if (name === "标点") {
                return value;
              }

              if (name === "最低价") {
                return value + " →";
              }

              if (name === "最高价") {
                return "← " + value;
              }
            },
          },

          data: [
            {
              name: "最高价",
              type: "max",
              valueDim: "highest",
              symbolOffset: [40, 0],
              itemStyle: {
                color: red,
              },
            },
            {
              name: "最低价",
              type: "min",
              valueDim: "lowest",
              symbolOffset: [-40, 0],
              itemStyle: {
                color: "rgb(41,60,85)",
              },
            },
          ],
        },
        markLine: {
          symbol: "",
          data: [
            {
              yAxis: data[data.length - 1].opening_price,
              label: {
                position: "end",
                padding: 0,
              },
              lineStyle: {
                type: "dotted",
                color: "#ccc",
              },
            },
          ],
        },
        itemStyle: {
          color: red,
          color0: green,
          borderColor: red,
          borderColor0: green,
        },
      },

      {
        type: "bar",
        name: "成交量",
        xAxisIndex: 1,
        yAxisIndex: 1,
        data: volumeData,
        barCategoryGap: "20%",
        itemStyle: {
          color(params) {
            const i = params.dataIndex;
            return data[i].closing_price > data[i].opening_price ? red : green;
          },
        },
      },

      {
        type: "bar",
        name: "MACD",
        xAxisIndex: 2,
        yAxisIndex: 2,
        data: macd,
        itemStyle: {
          color(params) {
            const data = params.data as number;
            return data >= 0 ? red : green;
          },
        },
      },

      {
        type: "line",
        name: "DIF",
        xAxisIndex: 2,
        yAxisIndex: 2,
        data: dif,
        showSymbol: false,
        lineStyle: {
          color: "white",
          width: 1,
        },
      },

      {
        type: "line",
        name: "DEA",
        xAxisIndex: 2,
        yAxisIndex: 2,
        showSymbol: false,
        data: dea,
        lineStyle: {
          color: "yellow",
          width: 1,
        },
      },
    ],
    legend: [
      {
        data: [],
        show: true,
        padding: 5,
        itemGap: 10,
        itemWidth: 25,
        itemHeight: 14,
      },
      {
        show: false,
        padding: 5,
        itemGap: 10,
        itemWidth: 25,
        itemHeight: 14,
      },
    ],

    grid: [
      {
        show: false,
        top: "60px",
        left,
        right,
        bottom: "35%",
        containLabel: true,
      },
      {
        show: false,
        left,
        right,
        top: "67%",
        bottom: "20%",
        containLabel: true,
      },
      {
        show: false,
        left,
        top: "82%",
        right,
        bottom: "30px",
        containLabel: true,
      },
    ],
  } as EChartsOption;
};
