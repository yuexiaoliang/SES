import { createApp } from 'vue';
import { createPinia } from 'pinia';

import  elementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'reset.css';

import App from './App.vue';
import { easyComponentsInstaller } from './easy-components';
import { themeInjecter } from './theme';
import { router } from '@/router/index'

import './styles/variables.scss';
import './styles/base.scss';

const app = createApp(App);

app.use(router)
app.use(createPinia());
app.use(elementPlus)
app.use(themeInjecter);
app.use(easyComponentsInstaller);

app.mount('#app');
