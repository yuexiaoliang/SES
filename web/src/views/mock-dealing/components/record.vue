<script setup lang="ts">
import { ref } from "vue";
import type {
  StockSimulatedTrading,
  StockSimulatedTradingRecord,
} from "@/apis/trading-test";

const emit = defineEmits<{
  (e: "onRecordAnchorClick", record: StockSimulatedTradingRecord): void;
}>();

defineProps<{
  data: StockSimulatedTrading;
}>();

const currentIndex = ref<number | null>(null);

const onItemClick = (item: StockSimulatedTradingRecord, index: number) => {
  currentIndex.value = index;
  emit("onRecordAnchorClick", item);
};
</script>

<template>
  <div class="mock-dealing-record">
    <header class="overview">
      <p>
        <span
          >总<b>{{ data.total_funds }}</b></span
        >
        |
        <span
          >剩<b>{{ data.balance }}</b></span
        >
        |
        <span
          >持<b> {{ data.intraday_holding_time }}</b></span
        >
        |
        <span
          >量<b>{{ data.holdings }}</b></span
        >
        |
        <span
          >市<b> {{ data.market_value }}</b></span
        >
      </p>
    </header>

    <div class="record">
      <ul class="record__list">
        <li
          v-for="(item, index) in data.records"
          class="record__list__item"
          :class="{
            'record__list__item--active': currentIndex === index,
          }"
        >
          <el-icon class="anchor el-icon-view" @click="onItemClick(item, index)"
            ><View
          /></el-icon>
          <p>类型：{{ item.type }}</p>
          <p>时间：{{ item.date }}</p>
          <p>单价：{{ item.price }}</p>
          <p>数量：{{ item.count }} 股</p>
          <p>总金额：{{ item.total }}</p>
          <p>剩余资金：{{ item.balance }}</p>
        </li>
      </ul>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.mock-dealing-record {
  display: flex;
  flex-direction: column;
  height: 100%;

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
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;

    &__list {
      @extend .scrollbar;
      flex: 1;
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
}
</style>
