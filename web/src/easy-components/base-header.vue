<script setup lang="ts">
const navList = [
  {
    name: "MockDealing",
    label: "模拟交易",
  },
  {
    name: "HistoricalAnalysis",
    label: "历史分析",
  },
];
</script>

<template>
  <div class="base-header">
    <!-- <theme-toggle-button /> -->
    <nav class="nav">
      <router-link
        v-for="nav in navList"
        :key="nav.name"
        :to="{ name: nav.name }"
        class="nav-item"
        >{{ nav.label }}</router-link
      >
    </nav>
  </div>
</template>

<style lang="scss" scoped>
.base-header {
  @include flex-center();

  height: var(--header-height);
  border-bottom: 1px solid var(--border-color);

  .nav {
    @include flex-center();
    .nav-item {
      margin: 0 10px;
      text-decoration: none;

      &.router-link-exact-active {
        color: yellow;
      }
    }
  }
}
</style>
