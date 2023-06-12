<script setup lang="ts">
import { ref } from "vue";
import { formatPrice } from "@/utils/common";
import { useStockList } from "@/hooks/stock";
import { Stock } from "@/apis/typings";

const emit = defineEmits<{
  (e: "onStockClick", stock: Stock): void;
  (e: "onFirstLoaded", stocks: Stock[]): void;
}>();

const { list, loading: listLoading } = useStockList(emit);
const columns = ref([
  {
    prop: "stock_name",
    label: "名称",
    fixed: true,
    minWidth: 80,
  },
  {
    prop: "latest_price",
    label: "最新",
    minWidth: 50,
    align: "center",
  },
  {
    prop: "previous_closing_price",
    label: "昨收",
    minWidth: 50,
    align: "center",
  },
  {
    prop: "total_market_value",
    label: "市值(亿)",
    minWidth: 60,
    align: "center",
  },
]);
</script>

<template>
  <div class="mock-dealing-list">
    <el-table v-loading="listLoading" :data="list" height="100%">
      <el-table-column v-for="col in columns" v-bind="col">
        <template #default="{ row, column }">
          <template v-if="column.property === 'stock_name'">
            <span class="name" @click="emit('onStockClick', row)">{{
              row[column.property]
            }}</span>
          </template>

          <template v-if="column.property === 'total_market_value'">{{
            formatPrice(row[column.property], "亿")
          }}</template>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<style lang="scss" scoped>
.mock-dealing-list {
  padding: 0 10px 10px;
  height: 100%;
  box-sizing: border-box;

  :deep(.el-table .el-table__cell) {
    padding: 0;
  }

  :deep(.el-table .cell) {
    padding: 0;
    font-size: 12px;
  }

  :deep(.el-table__header .cell) {
    padding: 5px 0;
    font-size: 14px;
  }

  .name {
    color: #a1a100;
    cursor: pointer;
  }
}
</style>
