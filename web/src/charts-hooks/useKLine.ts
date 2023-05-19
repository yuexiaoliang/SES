export default (data: []) => {
  const upColor = "#ec0000";
  const upBorderColor = "#8A0000";
  const downColor = "#00da3c";
  const downBorderColor = "#008F28";

  const categoryData = data.map((item: any) => {
    return item[0];
  });

  const values = data.map((item: any) => {
    return [item[1], item[2], item[3], item[4]];
  });

  function calculateMA(dayCount) {
    var result = [];
    for (var i = 0, len = values.length; i < len; i++) {
      if (i < dayCount) {
        result.push("-");
        continue;
      }
      var sum = 0;
      for (var j = 0; j < dayCount; j++) {
        sum += +values[i - j][1];
      }
      result.push(sum / dayCount);
    }
    return result;
  }

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
      data: ["日K", "MA5", "MA10", "MA20", "MA30"],
    },
    grid: {
      left: "10%",
      right: "10%",
      bottom: "15%",
    },
    xAxis: {
      type: "category",
      data: categoryData,
      boundaryGap: false,
      axisLine: { onZero: false },
      splitLine: { show: false },
      min: "dataMin",
      max: "dataMax",
    },
    yAxis: {
      scale: true,
      splitArea: {
        show: true,
      },
    },
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
        data: values,
        itemStyle: {
          color: upColor,
          color0: downColor,
          borderColor: upBorderColor,
          borderColor0: downBorderColor,
        },
        markPoint: {
          label: {
            formatter: function (param) {
              return param != null ? Math.round(param.value) + "" : "";
            },
          },
          data: [
            {
              name: "Mark",
              coord: ["2013/5/31", 2300],
              value: 2300,
              itemStyle: {
                color: "rgb(41,60,85)",
              },
            },
            {
              name: "highest value",
              type: "max",
              valueDim: "highest",
            },
            {
              name: "lowest value",
              type: "min",
              valueDim: "lowest",
            },
            {
              name: "average value on close",
              type: "average",
              valueDim: "close",
            },
          ],
          tooltip: {
            formatter: function (param) {
              return param.name + "<br>" + (param.data.coord || "");
            },
          },
        },
        markLine: {
          symbol: ["none", "none"],
          data: [
            [
              {
                name: "from lowest to highest",
                type: "min",
                valueDim: "lowest",
                symbol: "circle",
                symbolSize: 10,
                label: {
                  show: false,
                },
                emphasis: {
                  label: {
                    show: false,
                  },
                },
              },
              {
                type: "max",
                valueDim: "highest",
                symbol: "circle",
                symbolSize: 10,
                label: {
                  show: false,
                },
                emphasis: {
                  label: {
                    show: false,
                  },
                },
              },
            ],
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
        name: "MA5",
        type: "line",
        data: calculateMA(5),
        smooth: true,
        lineStyle: {
          opacity: 0.5,
        },
      },
      {
        name: "MA10",
        type: "line",
        data: calculateMA(10),
        smooth: true,
        lineStyle: {
          opacity: 0.5,
        },
      },
      {
        name: "MA20",
        type: "line",
        data: calculateMA(20),
        smooth: true,
        lineStyle: {
          opacity: 0.5,
        },
      },
      {
        name: "MA30",
        type: "line",
        data: calculateMA(30),
        smooth: true,
        lineStyle: {
          opacity: 0.5,
        },
      },
    ],
  };
};
