<script setup lang="ts">
import { ref } from "vue";
import { getStockDailyData } from "@/apis/stock";
import StockCandlestick from "@/components/stock-candlestick/stock-candlestick.vue";
import { StockHistory } from "@/apis/typings";
import { filterDataByPriceChgPctAndDateRange, filterDataByPriceChange } from "@/utils/filter";

const chartData = ref<StockHistory[]>([]);

const load = async () => {
  const { data } = await getStockDailyData("600288", {
    start_date: "2020-01-01",
  });

  const d = filterDataByPriceChange(data, 5, 3, true);
  chartData.value = data
};

load();
</script>

<template>
  <div class="home-view">
    <StockCandlestick :data="chartData"></StockCandlestick>
  </div>
</template>

<style lang="scss" scoped>
.home-view {
  padding-top: 200px;
}
</style>
