<script setup lang="ts">
import { ref } from "vue";
import { getStockDailyData } from "@/apis/stock";
import { Stock, StockHistory } from "@/apis/typings";
import StockCandlestick from "@/components/stock-candlestick/stock-candlestick.vue";
import HomeList from "./home-list.vue";
import { tradingTest, TradingRecord } from "@/utils/trading-test";

import data, { stock } from "./mock";

const chartData = ref<StockHistory[]>([]);

const load = async () => {
  const { data } = await getStockDailyData("002103", {
    // start_date: "2021-01-01",
  });

  // const d = convertUPFields(addMAToData(data, [5, 10, 20, 50, 100, 200]), 5);
  chartData.value = data;
};

const record = ref<TradingRecord[]>([]);

if (true) {
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
  console.log(stock);
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
      <ul>
        <li v-for="{ buy, sell } in record">
          <br />
          <p>买入时间：{{ buy.date }}</p>
          <p>买入单价：{{ buy.price }}</p>
          <p>买入数量：{{ buy.holdings }} 股</p>
          <p>买入总金额：{{ buy.total }}</p>
          <p>买入后剩余资金：{{ buy.availableFunds }}</p>

          <template v-if="sell">
            <p>卖出时间：{{ sell.date }}</p>
            <p>卖出单价：{{ sell.price }}</p>
            <p>卖出数量：{{ sell.holdings }} 股</p>
            <p>卖出总金额：{{ sell.total }}</p>
            <p>卖出后剩余资金：{{ sell.availableFunds }}</p>
            <p>持仓天数：{{ sell.holdingTime }} 天</p>
            <p>收益率：{{ sell.gainRatio }} %</p>
            <p>利润：{{ sell.profit }}</p>
          </template>
        </li>
      </ul>
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
