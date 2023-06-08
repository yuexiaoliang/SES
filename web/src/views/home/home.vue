<script setup lang="ts">
import { ref } from "vue";
import StockCandlestick from "@/components/stock-candlestick/stock-candlestick.vue";
import PieChart from "@/components/pie-chart/pie-chart.vue";
import { getStockDailyData } from "@/apis/stock";
import { StockHistory } from "@/apis/typings";
import { addMAToData, convertUPFields } from "@/utils/data-tools";
import { generateMultipleArray } from "@/utils/common";

import data from "./mock";

const chartData = ref<StockHistory[]>([]);

const load = async () => {
  const { data } = await getStockDailyData("002103", {
    // start_date: "2021-01-01",
  });

  // const d = convertUPFields(addMAToData(data, [5, 10, 20, 50, 100, 200]), 5);
  chartData.value = data
};

if (true) {
  // const d = convertUPFields(addMAToData(data, [5, 10, 20, 50, 100, 200]), 5);

  setTimeout(() => {
    chartData.value = data
  }, 100);
} else {
  load();
}
</script>

<template>
  <div class="home-view">
    <StockCandlestick
      width="100vw"
      height="100vh"
      :data="chartData"
    ></StockCandlestick>
  </div>
</template>

<style lang="scss" scoped>
.home-view {
}
</style>
