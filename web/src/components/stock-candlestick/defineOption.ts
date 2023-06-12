import { StockHistoryWithAny } from "@/apis/typings";
import { EChartsOption } from "echarts";

export default (data: StockHistoryWithAny[]) => {
  const dataZoomStart = data.length - 120;
  const dataZoomEnd = data.length;

  const left = 20;
  const right = 20;

  const red = "#FD1050";
  const green = "#0CF49B";
  const backgroundColor = "#000";
  const color = "#4a657a";

  // X 轴数据
  const xAxis = data.map((item: any) => item.date);

  // K 线数据
  const candlestickData = data.map((item) => [
    item.opening_price,
    item.closing_price,
    item.lowest_price,
    item.highest_price,
  ]);

  // 成交量
  const volumeData = data.map((item) => item.transaction_volume);

  const macd = data.map((item) => item.macd);
  const dif = data.map((item) => item.dif);
  const dea = data.map((item) => item.dea);

  const ma5 = data.map((item) => item.ma5);
  const ma10 = data.map((item) => item.ma10);
  const ma20 = data.map((item) => item.ma20);

  const buyPointData = data
    .filter((item) => item.buyRecord || item.sellRecord)
    .map((item) => {
      const { buyRecord, sellRecord } = item;

      const label = {
        show: true,
        formatter: buyRecord ? "B" : "S",
        color: buyRecord ? red : green,
        fontSize: 14,
        fontWeight: "bold",
        textShadowColor: buyRecord ? red : green,
        textShadowBlur: 5,
      };

      const result = {
        name: "标点",
        value: buyRecord ? buyRecord.price : sellRecord.price,
        coord: [item.date, item.lowest_price],
        symbol: "circle",
        symbolSize: 0,
        symbolOffset: [0, 15],
        label,
        emphasis: {
          disabled: true,
        },
      };

      return result;
    });

  return {
    backgroundColor,
    title: {
      text: data[0].stock_name,
      color,
    },

    tooltip: {
      show: true,
      trigger: "axis",
      triggerOn: "mousemove|click",
      axisPointer: {
        type: "cross",
      },
    },

    xAxis: [
      {
        show: true,
        scale: true,
        gridIndex: 0,
        axisTick: {
          show: false,
        },
        axisLabel: {
          margin: 15,
        },
        data: xAxis,
      },
      {
        show: true,
        scale: true,
        gridIndex: 1,
        axisLabel: {
          show: false,
        },
        axisTick: {
          show: false,
        },
        axisPointer: {
          label: {
            show: false,
          },
        },
        data: xAxis,
      },
      {
        show: true,
        scale: true,
        gridIndex: 2,
        axisLine: {
          show: false,
        },
        axisLabel: {
          show: false,
        },
        axisTick: {
          show: false,
        },
        axisPointer: {
          label: {
            show: false,
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
            color,
          },
        },
        axisLabel: {
          inside: true,
          margin: 0,
          showMinLabel: true,
          fontWeight: "bold",
          padding: [0, 0, 3, 0],
          verticalAlign: "bottom",
        },
        splitLine: {
          lineStyle: {
            dashOffset: 0,
            color: color,
            type: "dashed",
          },
        },
      },
      {
        position: "right",
        gridIndex: 1,
        minInterval: 0,
        axisLine: {
          show: false,
        },

        axisTick: {
          show: false,
        },

        axisLabel: {
          show: false,
        },

        splitLine: {
          show: false,
        },
      },
      {
        position: "right",
        gridIndex: 2,
        axisLine: {
          show: false,
        },

        axisTick: {
          show: false,
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
        startValue: dataZoomStart,
        endValue: dataZoomEnd,
        xAxisIndex: [0, 0],
        rangeMode: ["value", "value"],
      },
      {
        show: false,
        type: "inside",
        startValue: dataZoomStart,
        endValue: dataZoomEnd,
        xAxisIndex: [0, 1],
        rangeMode: ["value", "value"],
      },
      {
        show: false,
        type: "inside",
        startValue: dataZoomStart,
        endValue: dataZoomEnd,
        xAxisIndex: [0, 2],
        rangeMode: ["value", "value"],
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
        name: "K线图",
        type: "candlestick",
        xAxisIndex: 0,
        yAxisIndex: 0,
        data: candlestickData,
        markPoint: {
          label: {
            show: true,
            fontSize: 12,
            color: "#fff",
            formatter(param) {
              const { name, value } = param;

              if (name === "最低价") {
                return value + " →";
              }

              if (name === "最高价") {
                return "← " + value;
              }

              return value;
            },
          },

          data: [
            {
              name: "最高价",
              type: "max",
              valueDim: "highest",
              symbolOffset: [40, 0],
              symbol: "circle",
              symbolSize: 0,
            },
            {
              name: "最低价",
              type: "min",
              valueDim: "lowest",
              symbolOffset: [-40, 0],
              symbolSize: 0,
            },
            ...buyPointData,
          ],
        },
        markLine: {
          symbol: ["none", "none"],
          label: {
            show: false,
          },
          lineStyle: {
            type: "dotted",
          },
          data: [
            {
              yAxis: data[data.length - 1].opening_price,
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
        name: "MA5",
        xAxisIndex: 0,
        yAxisIndex: 0,
        data: ma5,
        symbol: "none",
        lineStyle: {
          width: 1,
        },
      },

      {
        type: "line",
        name: "MA10",
        xAxisIndex: 0,
        yAxisIndex: 0,
        data: ma10,
        symbol: "none",
        lineStyle: {
          width: 1,
        },
      },

      {
        type: "line",
        name: "MA20",
        xAxisIndex: 0,
        yAxisIndex: 0,
        data: ma20,
        symbol: "none",
        lineStyle: {
          width: 1,
        },
      },

      {
        type: "line",
        name: "DIF",
        xAxisIndex: 2,
        yAxisIndex: 2,
        data: dif,
        symbol: "none",
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
        symbol: "none",
        data: dea,
        lineStyle: {
          color: "yellow",
          width: 1,
        },
      },
    ],
    legend: [
      {
        data: ["MA5", "MA10", "MA20"],
        show: true,
        textStyle: {
          color: "#fff",
          lineHeight: 20,
        },
        top: 10,
        itemWidth: 15,
        itemHeight: 10,
        icon: "roundRect",
      },
      {
        show: false,
      },
    ],

    grid: [
      {
        show: false,
        top: 0,
        left,
        right,
        bottom: "40%",
        containLabel: true,
      },
      {
        show: false,
        left,
        right,
        top: "60.5%",
        bottom: "18.5%",
        containLabel: true,
      },
      {
        show: false,
        left,
        top: "82%",
        right,
        bottom: 0,
        containLabel: true,
      },
    ],
  } as EChartsOption;
};
