<script setup lang="ts">
</script>

<template>
  <div class="base-header">
    <theme-toggle-button />
  </div>
</template>

<style lang="scss" scoped>
.base-header {
  @include flex-center();

  height: var(--header-height);
  border-bottom: 1px solid var(--border-color);
}
</style>
