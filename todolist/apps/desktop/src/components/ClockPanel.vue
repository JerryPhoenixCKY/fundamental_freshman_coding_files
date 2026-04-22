<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from "vue";

const now = ref(new Date());
let timer: number | undefined;

onMounted(() => {
  timer = window.setInterval(() => {
    now.value = new Date();
  }, 1000);
});

onUnmounted(() => {
  if (timer !== undefined) {
    window.clearInterval(timer);
  }
});

const displayTime = computed(() =>
  now.value.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" })
);

const displayDate = computed(() =>
  now.value.toLocaleDateString([], { weekday: "long", year: "numeric", month: "short", day: "numeric" })
);
</script>

<template>
  <section class="clock-panel">
    <p class="clock-label">Desk Time</p>
    <p class="clock-time">{{ displayTime }}</p>
    <p class="clock-date">{{ displayDate }}</p>
  </section>
</template>
