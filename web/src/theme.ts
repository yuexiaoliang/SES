import { Plugin } from 'vue';

export const theme = {
  'dark': {
    '--primary': 'blue'
  },

  'light': {
    '--primary': 'green'
  }
};

export const themeInjecter: Plugin = {
  install() {
    Object.entries(theme).forEach(([name, variables]) => {
      const styleEle = document.createElement('style');

      styleEle.setAttribute('theme-name', name);

      const styleText = Object.entries(variables)
        .map(([key, value]) => `${key}: ${value};`)
        .join('\n');

      styleEle.innerHTML = `:root[theme="${name}"] {\n${styleText}\n}`;
      document.head.appendChild(styleEle);
    });
  }
};