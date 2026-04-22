<script setup lang="ts">
import type { TaskItem } from "../types";

defineProps<{
  loading: boolean;
  tasks: TaskItem[];
}>();

const emit = defineEmits<{
  toggle: [id: string];
  remove: [id: string];
}>();

function formatDate(value?: string): string {
  if (!value) {
    return "-";
  }
  return new Date(value).toLocaleString();
}
</script>

<template>
  <section class="todo-list">
    <header class="list-header">
      <h2>Today Queue</h2>
    </header>

    <p v-if="loading" class="status">Loading tasks...</p>
    <p v-else-if="tasks.length === 0" class="status">No tasks yet. Add one above.</p>

    <ul v-else>
      <li v-for="task in tasks" :key="task.id" class="task-item">
        <div class="task-main">
          <button class="check-btn" :class="{ done: task.completed }" @click="emit('toggle', task.id)">
            {{ task.completed ? "Done" : "Todo" }}
          </button>
          <div>
            <p class="task-title" :class="{ done: task.completed }">{{ task.title }}</p>
            <p class="task-meta">priority: {{ task.priority }} | due: {{ formatDate(task.dueAt) }}</p>
            <p class="task-meta">reminder: {{ formatDate(task.remindAt) }}</p>
          </div>
        </div>

        <button class="danger-btn" @click="emit('remove', task.id)">Delete</button>
      </li>
    </ul>
  </section>
</template>
