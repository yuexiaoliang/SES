<script setup lang="ts">
import { ref } from "vue";
import { getStockDailyData } from "@/apis/stock";
import StockCandlestick from "@/components/stock-candlestick/stock-candlestick.vue";
import { StockHistory } from "@/apis/typings";
import { filterDataByPriceChgPctAndDateRange } from "@/utils/filter";

const chartData = ref<StockHistory[]>([]);

const load = async () => {
  const { data } = await getStockDailyData("601390", {
    start_date: "2022-01-01",
  });

  chartData.value = filterDataByPriceChgPctAndDateRange(data, 5, 3, true);
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
