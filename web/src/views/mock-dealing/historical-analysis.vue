<script setup lang="ts">
import { getTradingTestStocks } from "@/apis/trading-test";

import data, { codes } from "./mock.js";
import { chunkArray } from "@/utils/common";

// 1. 柱状图来表示每月盈利
// 2. 饼图表示以年或 n 年为单位的收益比例
// 3. 矩形树图表示各股票的收益
// 4. 有个收益排名版块
// 5. 盈利和亏损可以用日历图（类似github提交）表示，每个日期有多少股票盈利多少股票亏损

const result = [];
const codesList = chunkArray(codes, 3);

getTradingTestStocks({
  raw_funds: 10000,
  start_date: "2022-01-01",
  stocks: codes,
})
  .then((res) => {
    console.log(
      `🚀 > file: historical-analysis.vue:25 > Promise.all > res:`,
      res
    );
  })
  .catch((err) => {
    console.log(
      `🚀 > file: historical-analysis.vue:30 > Promise.all > err:`,
      err
    );
  });

// const requestList = codesList.map((codes) => {
//   return getTradingTestStocks({
//     raw_funds: 10000,
//     start_date: "2022-01-01",
//     stocks: codes.join(","),
//   });
// });

// Promise.all(requestList)
//   .then((res) => {
//     console.log(
//       `🚀 > file: historical-analysis.vue:25 > Promise.all > res:`,
//       res
//     );
//   })
//   .catch((err) => {
//     console.log(
//       `🚀 > file: historical-analysis.vue:30 > Promise.all > err:`,
//       err
//     );
//   });

const load = () => {
  const codesList = [[], []];
  // getTradingTestStocks
};
</script>

<template>
  <div class="historical-analysis">historical-analysis</div>
</template>

<style lang="scss" scoped>
.historical-analysis {
}
</style>
