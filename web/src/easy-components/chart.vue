<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import * as echarts from "echarts";

interface Props {
  option: Option;
}

interface Option {}

const props = defineProps<Props>();

const chatRef = ref();
const chart = ref();

onMounted(() => {
  chart.value = echarts.init(chatRef.value);
  chart.value.setOption(props.option);
});

watch(
  () => props.option,
  () => {
    setOption();
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
  chart.value.setOption(props.option);
}

function setOption() {
  chart.value.setOption(props.option);
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
  width: 1000px;
  height: 500px;
}
</style>
