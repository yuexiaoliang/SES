<script setup lang="ts">
import { ref } from "vue";
import { getStockDailyData } from "@/apis/stock";
import { Stock, StockHistory } from "@/apis/typings";
import StockCandlestick from "@/components/stock-candlestick/stock-candlestick.vue";
import { tradingTest, TradingRecord } from "@/utils/trading-test";

import List from "./components/list.vue";
import Record, { RecordAnchorType } from "./components/record.vue";

const chartData = ref<StockHistory[]>([]);

const load = async (stock: Stock) => {
  const { data } = await getStockDailyData(stock.stock_code);

  const [_record, _data] = tradingTest(stock, data);
  chartData.value = _data;
  records.value = _record;
};

const onListFirstLoaded = (stocks: Stock[]) => {
  const firstStock = stocks[0];
  load(firstStock);
};

const records = ref<TradingRecord[]>([]);

const onStockClick = (stock: Stock) => {
  load(stock);
};

const candlestickChart = ref();
const onRecordAnchorClick = (record: TradingRecord) => {
  const buyDate = record.buy.date;
  const sellDate = record.sell?.date;

  const startIndex = chartData.value.findIndex(
    (dataItem) => dataItem.date === buyDate
  );

  const endIndex = chartData.value.findIndex((dataItem) => {
    if (!sellDate) return;

    return dataItem.date === sellDate;
  });

  const startValue = startIndex - 20;
  const endValue = endIndex > -1 ? endIndex + 20 : startIndex + 20;

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
        :record="records"
        @onRecordAnchorClick="onRecordAnchorClick"
      ></Record>
    </aside>
  </div>
</template>

<style lang="scss" scoped>
.mock-dealing {
  display: flex;
  width: 100vw;
  height: 100vh;

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
