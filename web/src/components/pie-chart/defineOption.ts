import { StockHistoryWithAny } from "@/apis/typings";
import { EChartsOption } from "echarts";

export default (data: StockHistoryWithAny[]) => {
  const maKeys = Object.keys(data[0]).filter((key) => key.startsWith("ma_"));

  const filtered: StockHistoryWithAny[] = [];
  data.forEach((item, index) => {
    if (!item.raise) return;

    // 当item所有的maKeys都有值
    if (maKeys.every((key) => item[key])) {
      filtered.push(data[index - 1]);
    }
  });

  const d: Record<string, any> = {};
  filtered.forEach((item) => {
    for (const key in item) {
      const v = item[key];

      if (!key.startsWith("ma_")) continue;
      if (!item[key]) continue;

      // if (v > item.closing_price) continue;

      if (!d[key]) {
        d[key] = {
          valueCount: 0,
          up: 0,
          upArr: [],
          down: 0,
          downArr: [],
        };
      }

      const o = d[key];
      o.valueCount += 1;
      if (v < item.closing_price) {
        o.up += 1;
        o.upArr.push(item.change_percent);
      } else {
        o.down += 1;
        o.downArr.push(item.change_percent);
      }
    }
  });

  console.log(filtered, d);
  return {
    title: {
      text: "Referer of a Website",
      subtext: "Fake Data",
      left: "center",
    },
    tooltip: {
      trigger: "item",
    },
    legend: {
      orient: "vertical",
      left: "left",
    },
    series: [
      {
        name: "Access From",
        type: "pie",
        radius: "50%",
        data: [
          { value: 1048, name: "Search Engine" },
          { value: 735, name: "Direct" },
          { value: 580, name: "Email" },
          { value: 484, name: "Union Ads" },
          { value: 300, name: "Video Ads" },
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: "rgba(0, 0, 0, 0.5)",
          },
        },
      },
    ],
  } as EChartsOption;
};
