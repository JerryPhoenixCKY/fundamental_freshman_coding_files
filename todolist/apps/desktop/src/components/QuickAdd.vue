<script setup lang="ts">
import { reactive } from "vue";
import type { CreateTaskInput, TaskPriority } from "../types";

const emit = defineEmits<{
  submit: [payload: CreateTaskInput];
}>();

const form = reactive<CreateTaskInput>({
  title: "",
  notes: "",
  dueAt: "",
  remindAt: "",
  priority: "medium"
});

function submit() {
  if (!form.title.trim()) {
    return;
  }

  emit("submit", {
    title: form.title.trim(),
    notes: form.notes?.trim() || undefined,
    dueAt: form.dueAt || undefined,
    remindAt: form.remindAt || undefined,
    priority: form.priority
  });

  form.title = "";
  form.notes = "";
  form.dueAt = "";
  form.remindAt = "";
  form.priority = "medium";
}

const priorities: TaskPriority[] = ["low", "medium", "high"];
</script>

<template>
  <form class="quick-add" @submit.prevent="submit">
    <input v-model="form.title" class="field" placeholder="Add a task title" required />
    <textarea v-model="form.notes" class="field field-notes" placeholder="Notes (optional)" />

    <div class="row two-col">
      <label>
        <span>Due</span>
        <input v-model="form.dueAt" class="field" type="datetime-local" />
      </label>
      <label>
        <span>Reminder</span>
        <input v-model="form.remindAt" class="field" type="datetime-local" />
      </label>
    </div>

    <div class="row action-row">
      <label>
        <span>Priority</span>
        <select v-model="form.priority" class="field">
          <option v-for="p in priorities" :key="p" :value="p">{{ p }}</option>
        </select>
      </label>
      <button class="primary-btn" type="submit">Add</button>
    </div>
  </form>
</template>
