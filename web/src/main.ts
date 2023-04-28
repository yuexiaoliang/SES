import { createApp } from 'vue';
import { createPinia } from 'pinia';

import App from './App.vue';

import { themeInjecter } from './theme';

import 'reset.css';

const app = createApp(App);

app.use(createPinia());
app.use(themeInjecter);

app.mount('#app');
