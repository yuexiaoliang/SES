<script setup lang="ts">
import { ref } from "vue";
import { getStockDailyData } from "@/apis/stock";
import { getTradingTestSingle } from "@/apis/trading-test";
import type { StockSimulatedTrading, StockSimulatedTradingRecord } from "@/apis/trading-test";
import { Stock, StockHistory } from "@/apis/typings";
import { addBSToData } from "@/utils/trading-test";
import StockCandlestick from "@/components/stock-candlestick/stock-candlestick.vue";

import List from "./components/list.vue";
import Record from "./components/record.vue";

const chartData = ref<StockHistory[]>([]);

const load = async (stock: Stock) => {
  const { data: testData } = await getTradingTestSingle(stock.stock_code, {
    start_date: "2023-01-01",
    raw_funds: 10000,
  });

  const { data } = await getStockDailyData(stock.stock_code, {
    start_date: "2023-01-01",
  });

  chartData.value = addBSToData(data, testData.records);
  records.value = testData;
};

const onListFirstLoaded = (stocks: Stock[]) => {
  const firstStock = stocks[0];
  load(firstStock);
};

const records = ref<StockSimulatedTrading>();

const onStockClick = (stock: Stock) => {
  load(stock);
};

const candlestickChart = ref();
const onRecordAnchorClick = (record: StockSimulatedTradingRecord) => {
  const date = record.date;

  const index = chartData.value.findIndex(
    (dataItem) => dataItem.date === date
  );

  const startValue = index - 20;
  const endValue = index > -1 ? index + 20 : index + 20;

  candlestickChart.value.setDataZoom(startValue, endValue);
};
</script>

<template>
  <div class="mock-dealing">
    <aside class="mock-dealing__side mock-dealing__side--left">
      <List
        @onStockClick="onStockClick"
        @onFirstLoaded="onListFirstLoaded"
      ></List>
    </aside>

    <section class="mock-dealing__content">
      <StockCandlestick
        ref="candlestickChart"
        width="100%"
        height="100%"
        :data="chartData"
      ></StockCandlestick>
    </section>

    <aside class="mock-dealing__side mock-dealing__side--right">
      <Record
        :data="records"
        @onRecordAnchorClick="onRecordAnchorClick"
      ></Record>
    </aside>
  </div>
</template>

<style lang="scss" scoped>
.mock-dealing {
  display: flex;
  width: 100%;
  height: 100%;

  &__side {
    @extend .scrollbar;

    flex-shrink: 0;
    width: 240px;
    height: 100%;
    border-color: var(--border-color);
    border-width: 0px;
    border-style: solid;
    box-sizing: border-box;

    &--left {
      width: 270px;
      border-right-width: 1px;
    }

    &--right {
      border-left-width: 1px;
    }
  }

  &__content {
    @extend .scrollbar;
    flex: 1;
    padding: 10px;
  }
}
</style>
