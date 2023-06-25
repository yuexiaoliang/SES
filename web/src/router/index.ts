import { createRouter, createWebHistory } from "vue-router";
import type { RouterOptions } from "vue-router";

const routes: RouterOptions["routes"] = [
  {
    name: "Home",
    path: "/",
    redirect: { name: "MockDealing" },
  },
  {
    name: "MockDealing",
    path: "/mock-dealing",
    component: () => import("@/views/mock-dealing/mock-dealing.vue"),
  },
  {
    name: "HistoricalAnalysis",
    path: "/historical-analysis",
    component: () => import("@/views/mock-dealing/historical-analysis.vue"),
  }
];

export const router = createRouter({
  routes,
  history: createWebHistory(),
});
