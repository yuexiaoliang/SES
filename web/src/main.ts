import { createApp } from "vue";
import { createPinia } from "pinia";

import elementPlus from "element-plus";
import "element-plus/dist/index.css";
import "element-plus/theme-chalk/dark/css-vars.css";
import "reset.css";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";

import App from "./App.vue";
import { easyComponentsInstaller } from "./easy-components";
import { themeInjecter } from "./theme";
import { router } from "@/router/index";

import "./styles/variables.scss";
import "./styles/base.scss";

const app = createApp(App);
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

app.use(router);
app.use(createPinia());
app.use(elementPlus);
app.use(themeInjecter);
app.use(easyComponentsInstaller);

app.mount("#app");
