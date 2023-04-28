import { computed, watchEffect } from 'vue';
import { defineStore } from 'pinia';
import { useColorMode, useCycleList } from '@vueuse/core';
import { theme } from '@/theme';

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

  return { toggleTheme: next, themeMode: state, variables };
});
