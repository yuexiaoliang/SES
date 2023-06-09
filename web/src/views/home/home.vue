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
    chartData.value = data;

    record.value = tradingTest(stock, data);
    console.log(
      `🚀 > file: home.vue:30 > setTimeout > record.value:`,
      record.value
    );
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
        <li v-for="item in record" :key="item.date">
          <br />
          <p>类型：{{ item.type }}</p>
          <p>时间：{{ item.date }}</p>
          <p>单价：{{ item.price }}</p>
          <p>数量：{{ item.holdings }} 股</p>
          <p>总金额：{{ item.total }}</p>
          <p>剩余可用资金：{{ item.availableFunds }}</p>

          <template v-if="item.type === '卖出'">
            <p>持仓天数：{{ item.holdingTime }} 天</p>
            <p>收益率：{{ item.gainRatio }} %</p>
            <p>利润：{{ item.profit }}</p>
            <hr />
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
