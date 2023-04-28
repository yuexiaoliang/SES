<script setup lang="ts">
import { useTheme } from '@/stores/theme';

const { toggleTheme } = useTheme();
</script>

<template>
  <div class="div" @click="toggleTheme()">123</div>
</template>

<style scoped>
.div {
  background-color: var(--primary);
}
</style>
