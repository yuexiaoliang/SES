<script setup lang="ts">
import { storeToRefs } from 'pinia';
import { useTheme } from '@/stores/theme';

const themeStore = useTheme();

const { toggle: toggleTheme } = themeStore;
const { icon: ThemeIcon } = storeToRefs(themeStore);
</script>

<template>
  <el-icon class="theme-toggle-button" @click="toggleTheme()"><ThemeIcon></ThemeIcon></el-icon>
</template>

<style lang="scss" scoped>
.theme-toggle-button {
  font-size: 20px;
  color: var(--color);
  cursor: pointer;
}
</style>
