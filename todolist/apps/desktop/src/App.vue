<script setup lang="ts">
import { onMounted, ref } from "vue";
import ClockPanel from "./components/ClockPanel.vue";
import QuickAdd from "./components/QuickAdd.vue";
import TodoList from "./components/TodoList.vue";
import { useReminderEngine } from "./composables/useReminderEngine";
import { createTask, fetchTasks, removeTask, toggleTask } from "./api";
import type { CreateTaskInput, TaskItem } from "./types";

const tasks = ref<TaskItem[]>([]);
const loading = ref(false);
const error = ref("");
const { notices, dismissNotice } = useReminderEngine(tasks);

async function loadTasks() {
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
  void loadTasks();
});
</script>

<template>
  <main class="app-shell">
    <section class="left-column">
      <ClockPanel />
      <QuickAdd @submit="handleCreate" />
    </section>

    <section class="right-column">
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
