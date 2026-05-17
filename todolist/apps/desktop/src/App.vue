<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import ClockPanel from "./components/ClockPanel.vue";
import QuickAdd from "./components/QuickAdd.vue";
import TodoList from "./components/TodoList.vue";
import AuthPanel from "./components/AuthPanel.vue";
import { useReminderEngine } from "./composables/useReminderEngine";
import { createTask, fetchTasks, removeTask, toggleTask } from "./api";
import type { CreateTaskInput, TaskItem } from "./types";

const token = ref(localStorage.getItem("token") || "");
const tasks = ref<TaskItem[]>([]);
const loading = ref(false);
const error = ref("");
const { notices, dismissNotice } = useReminderEngine(tasks);

watch(token, (newVal) => {
  if (newVal) {
    localStorage.setItem("token", newVal);
    void loadTasks();
  } else {
    localStorage.removeItem("token");
    tasks.value = [];
  }
});

async function loadTasks() {
  if (!token.value) return;
  loading.value = true;
  error.value = "";
  try {
    tasks.value = await fetchTasks();
  } catch (err) {
    error.value = err instanceof Error ? err.message : "Failed to load tasks";
  } finally {
    loading.value = false;
  }
}

async function handleCreate(input: CreateTaskInput) {
  error.value = "";
  try {
    const task = await createTask(input);
    tasks.value = [task, ...tasks.value];
  } catch (err) {
    error.value = err instanceof Error ? err.message : "Failed to create task";
  }
}

async function handleToggle(id: string) {
  error.value = "";
  try {
    const updated = await toggleTask(id);
    tasks.value = tasks.value.map((task) => (task.id === id ? updated : task));
  } catch (err) {
    error.value = err instanceof Error ? err.message : "Failed to update task";
  }
}

async function handleRemove(id: string) {
  error.value = "";
  try {
    await removeTask(id);
    tasks.value = tasks.value.filter((task) => task.id !== id);
  } catch (err) {
    error.value = err instanceof Error ? err.message : "Failed to delete task";
  }
}

onMounted(() => {
  if (token.value) {
    void loadTasks();
  }
});
</script>

<template>
  <main class="app-shell relative">
    <div v-if="!token" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 overflow-hidden">
      <AuthPanel class="bg-white" @login="(t: string) => token = t" />
    </div>

    <section class="left-column opacity-30" :class="{ '!opacity-100': token }">
      <ClockPanel />
      <QuickAdd @submit="handleCreate" />
    </section>

    <div v-if="token" class="absolute top-4 right-4 flex gap-2 items-center">
      <button @click="token = ''" class="px-2 py-1 text-xs border rounded bg-white text-gray-700 hover:bg-gray-100">Sign Out</button>
    </div>

    <section class="right-column opacity-30" :class="{ '!opacity-100': token }">
      <section v-if="notices.length" class="reminder-stack">
        <article v-for="notice in notices" :key="notice.id" class="reminder-item">
          <div>
            <p class="reminder-title">Reminder</p>
            <p class="reminder-task">{{ notice.title }}</p>
            <p class="reminder-time">
              {{ notice.remindAt ? new Date(notice.remindAt).toLocaleString() : "Now" }}
            </p>
          </div>
          <button class="ghost-btn" @click="dismissNotice(notice.id)">Dismiss</button>
        </article>
      </section>

      <p v-if="error" class="error-banner">{{ error }}</p>
      <TodoList :loading="loading" :tasks="tasks" @toggle="handleToggle" @remove="handleRemove" />
    </section>
  </main>
</template>
