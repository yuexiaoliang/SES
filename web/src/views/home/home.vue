<script setup lang="ts">
import { ref } from "vue";
import StockCandlestick from "@/components/stock-candlestick/stock-candlestick.vue";
import PieChart from "@/components/pie-chart/pie-chart.vue";
import { getStockDailyData } from "@/apis/stock";
import { StockHistory } from "@/apis/typings";
import { addMAToData, convertUPFields } from "@/utils/data-tools";
import { generateMultipleArray } from "@/utils/common";

const chartData = ref<StockHistory[]>([]);

const load = async () => {
  const { data } = await getStockDailyData("600362", {
    start_date: "2011-01-01",
  });

  const d = convertUPFields(addMAToData(data, [5, 10, 20, 50, 100, 200]), 5);
  chartData.value = d;
};

load();
</script>

<template>
  <div class="home-view">
    <StockCandlestick :data="chartData"></StockCandlestick>
    <PieChart :data="chartData"></PieChart>
  </div>
</template>

<style lang="scss" scoped>
.home-view {
  padding-top: 200px;
}
</style>
