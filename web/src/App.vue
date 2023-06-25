<script setup lang="ts"></script>

<template>
  <base-header class="base-header" />

  <div class="base-main">
    <router-view />
  </div>
</template>

<style scoped>
.base-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
}

.base-main {
  position: fixed;
  top: var(--header-height);
  left: 0;
  right: 0;
  bottom: 0;
}
</style>
