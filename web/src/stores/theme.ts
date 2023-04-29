import { computed, watchEffect } from 'vue';
import { defineStore } from 'pinia';
import { useColorMode, useCycleList } from '@vueuse/core';
import { theme } from '@/theme';
import { Sunny, Moon } from '@element-plus/icons-vue'

export const useTheme = defineStore('theme', () => {
  const mode = useColorMode({
    storageKey: 'color-theme',
    selector: 'html',
    attribute: 'theme',
    modes: {
      dark: 'dark',
      light: 'light'
    }
  });

  const { state, next } = useCycleList(['light', 'dark'], { initialValue: mode });

  watchEffect(() => {
    mode.value = state.value as any;
  });

  const variables = computed(() => {
    // @ts-ignore
    return theme[state.value] || {};
  });

  const isDark = computed(() => state.value === 'dark');
  const isLight = computed(() => state.value === 'light');

  const icon = computed(() => {
    return isDark.value ? Sunny : Moon
  })

  return { toggle: next, mode: state, variables, isDark, isLight, icon };
});
