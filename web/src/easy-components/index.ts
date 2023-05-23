import type { Plugin } from 'vue';
import ThemeToggleButton from './theme-toggle-button.vue';
import BaseHeader from './base-header.vue';

const modules = { ThemeToggleButton, BaseHeader };

export const easyComponentsInstaller = {
  install(app) {
    Object.entries(modules).forEach((module) => {
      const [name, component] = module;
      app.component(name, component);
    });
  }
} as Plugin;
