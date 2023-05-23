<script setup lang="ts">
import * as echarts from "echarts";
import { onMounted, ref, watch, computed, shallowRef } from "vue";
import { StockHistory } from "@/apis/typings";
import defineOption from "./defineOption";

interface Props {
  data: StockHistory[];
}

const props = defineProps<Props>();

const chatRef = ref();
const chart = shallowRef();

const option = computed(() => {
  return defineOption(props.data);
});

onMounted(() => {
  chart.value = echarts.init(chatRef.value);

  setOption();
});

watch(
  () => props.data,
  () => {
    console.log(option.value);
    setOption();
  },
  {
    deep: true,
  }
);

defineExpose({
  chart,
  resize,
  dispose,
  setOption,
  getOption,
  reset,
});

function getOption() {
  return chart.value.getOption();
}

function reset() {
  chart.value.clear();
  chart.value.setOption(option.value);
}

function setOption() {
  chart.value.setOption(option.value);
}

function resize() {
  chart.value.resize();
}

function dispose() {
  chart.value.dispose();
}
</script>

<template>
  <div class="chat" ref="chatRef">chat</div>
</template>

<style lang="scss" scoped>
.chat {
  width: 800px;
  height: 300px;
}
</style>
