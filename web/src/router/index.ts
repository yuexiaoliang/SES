import { createRouter, createWebHistory } from "vue-router";
import type { RouterOptions } from "vue-router";
import Home from "@/views/home/home.vue";

const routes: RouterOptions["routes"] = [
  {
    name: "Home",
    path: "/",
    // component: Home,
    redirect: { name: "MockDealing" },
  },
  {
    name: "MockDealing",
    path: "/mock-dealing",
    component: () => import("@/views/mock-dealing/mock-dealing.vue"),
  },
];

export const router = createRouter({
  routes,
  history: createWebHistory(),
});
