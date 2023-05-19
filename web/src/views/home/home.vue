<script setup lang="ts">
import * as echarts from "echarts";
import { onMounted, ref, shallowRef } from "vue";
import { getStockDailyData } from "@/apis/stock";
import useKLine from "@/charts-hooks/useKLine";

const chart = shallowRef();
const chartRef = ref();

const load = async () => {
  const res = await getStockDailyData({
    code: "301231",
  });

  const data = res.data.map((item) => {
    const { date, closing, opening, lowest, highest } = item;
    return [date, opening, closing, lowest, highest];
  });

  const kLine = useKLine(data);
  console.log(`🚀 > file: home.vue:22 > load > kLine:`, kLine);

  chart.value.setOption(kLine);
};

onMounted(() => {
  chart.value = echarts.init(chartRef.value);

  load();
});
</script>

<template>
  <div class="home-view">
    <!-- <Chart ref="chartRef" :option="kLine"></Chart> -->
    <div style="width: 1000px; height: 500px" ref="chartRef"></div>
  </div>
</template>

<style lang="scss" scoped>
.home-view {
}
</style>
