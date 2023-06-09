<script setup lang="ts">
import { ref } from "vue";
import { getStockDailyData } from "@/apis/stock";
import { Stock, StockHistory } from "@/apis/typings";
import StockCandlestick from "@/components/stock-candlestick/stock-candlestick.vue";
import { tradingTest, TradingRecord } from "@/utils/trading-test";
import HomeList from "./home-list.vue";
import HomeRecord from "./home-record.vue";

import data, { stock } from "./mock";

const chartData = ref<StockHistory[]>([]);

const code = ref("002103");

const load = async () => {
  const { data } = await getStockDailyData(code.value, {
    // start_date: "2021-01-01",
  });

  // const d = convertUPFields(addMAToData(data, [5, 10, 20, 50, 100, 200]), 5);
  const [_record, _data] = tradingTest(stock, data);
  chartData.value = _data;
  record.value = _record;
};

const record = ref<TradingRecord[]>([]);

if (false) {
  // const d = convertUPFields(addMAToData(data, [5, 10, 20, 50, 100, 200]), 5);

  setTimeout(() => {
    const [_record, _data] = tradingTest(stock, data);
    chartData.value = _data;
    record.value = _record;
  }, 100);
} else {
  load();
}

const onStockClick = (stock: Stock) => {
  code.value = stock.stock_code;
  load();
};
</script>

<template>
  <div class="home">
    <aside class="home__side home__side--left">
      <HomeList @onStockClick="onStockClick"></HomeList>
    </aside>

    <section class="home__content">
      <StockCandlestick
        width="100%"
        height="100%"
        :data="chartData"
      ></StockCandlestick>
    </section>

    <aside class="home__side home__side--right">
      <HomeRecord :record="record"></HomeRecord>
    </aside>
  </div>
</template>

<style lang="scss" scoped>
.home {
  display: flex;
  width: 100vw;
  height: 100vh;

  &__side {
    @extend .scrollbar;

    flex-shrink: 0;
    padding: 10px;
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
  }
}
</style>
