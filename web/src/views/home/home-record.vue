<script setup lang="ts">
import { TradingRecord } from '@/utils/trading-test';

const props = defineProps<{
  record: TradingRecord[];
}>();
</script>

<template>
  <div class="home-record">
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
  </div>
</template>

<style lang="scss" scoped>
.home-record {
}
</style>
