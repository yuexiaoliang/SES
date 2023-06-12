<script setup lang="ts">
import { computed, ref } from "vue";
import { TradingRecord } from "@/utils/trading-test";
import { formatNumber } from "@/utils/formatter";

const emit = defineEmits<{
  (e: "onRecordAnchorClick", record: TradingRecord): void;
}>();

const props = defineProps<{
  record: TradingRecord[];
}>();

const record = computed(() => {
  return props.record.filter((item) => item.sell);
});

const overview = computed(() => {
  // 总次数
  const total = record.value.length;

  // 盈利次数
  const profit = record.value.filter(
    (item) => item.sell && item.sell.profit > 0
  ).length;

  // 亏损次数
  const loss = record.value.filter(
    (item) => item.sell && item.sell.profit < 0
  ).length;

  // 总盈利
  const totalProfit = formatNumber(
    record.value
      .filter((item) => item.sell)
      .reduce((prev, curr) => {
        return prev + curr.sell!.profit;
      }, 0),
    0
  );

  return {
    total,
    profit,
    loss,
    totalProfit,
  };
});

const currentIndex = ref<number | null>(null);

const onItemClick = (item: TradingRecord, index: number) => {
  currentIndex.value = index;
  emit("onRecordAnchorClick", item);
};
</script>

<template>
  <div class="mock-dealing-record">
    <header class="overview">
      <p>
        总<b>{{ overview.total }}</b> | 盈<b>{{ overview.profit }}</b> | 亏<b>{{
          overview.loss
        }}</b>
        | 利<b>{{ overview.totalProfit }}</b>
      </p>
    </header>

    <ul class="record">
      <li
        v-for="(item, index) in record"
        class="record__item"
        :class="{
          'record__item--active': currentIndex === index,
          'record__item--is-loss': item.sell?.profit && item.sell.profit < 0,
        }"
      >
        <el-icon class="anchor el-icon-view" @click="onItemClick(item, index)"
          ><View
        /></el-icon>
        <p>买入时间：{{ item.buy.date }}</p>
        <p>买入单价：{{ item.buy.price }}</p>
        <p>买入数量：{{ item.buy.holdings }} 股</p>
        <p>买入总金额：{{ item.buy.total }}</p>
        <p>买入后剩余资金：{{ item.buy.availableFunds }}</p>

        <template v-if="item.sell">
          <p>卖出时间：{{ item.sell.date }}</p>
          <p>卖出单价：{{ item.sell.price }}</p>
          <p>卖出数量：{{ item.sell.holdings }} 股</p>
          <p>卖出总金额：{{ item.sell.total }}</p>
          <p>卖出后剩余资金：{{ item.sell.availableFunds }}</p>
          <p>持仓天数：{{ item.sell.holdingTime }} 天</p>
          <p>收益率：{{ item.sell.gainRatio }} %</p>
          <p>利润：{{ item.sell.profit }}</p>
        </template>
      </li>
    </ul>
  </div>
</template>

<style lang="scss" scoped>
.mock-dealing-record {
  .overview {
    padding: 10px;
    border-bottom: 1px solid var(--border-color);
    font-size: 12px;

    b {
      padding: 0 5px;
      font-weight: bold;
      color: var(--color-yellow);
    }
  }

  .record {
    padding: 10px;

    &__item {
      position: relative;
      padding-bottom: 10px;
      margin-bottom: 10px;
      border-bottom: 1px solid var(--border-color);

      &:last-child {
        margin-bottom: 0;
        padding-bottom: 0;
        border-bottom: none;
      }

      &::after {
        content: "";
        position: absolute;
        right: 32px;
        top: 7px;
        width: 8px;
        height: 8px;
        border-radius: 4px;
      }

      &--is-loss {
        &::after {
          background-color: red;
          box-shadow: 0 0 8px 3px red;
        }
      }

      .anchor {
        position: absolute;
        top: 2px;
        right: 3px;
        line-height: 1;
        color: #fff;
        font-size: 18px;
        cursor: pointer;
      }
      &--active {
        .anchor {
          color: yellow;
        }
      }
    }
  }
}
</style>
