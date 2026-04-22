import type { CreateTaskInput, TaskItem } from "./types";

const API_BASE = import.meta.env.VITE_API_BASE ?? "http://localhost:3000/api";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {})
    },
    ...init
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export async function fetchTasks(): Promise<TaskItem[]> {
  return request<TaskItem[]>("/tasks");
}

export async function createTask(input: CreateTaskInput): Promise<TaskItem> {
  return request<TaskItem>("/tasks", {
    method: "POST",
    body: JSON.stringify(input)
  });
}

export async function toggleTask(id: string): Promise<TaskItem> {
  return request<TaskItem>(`/tasks/${id}/toggle`, {
    method: "PATCH"
  });
}

export async function removeTask(id: string): Promise<{ success: boolean }> {
  return request<{ success: boolean }>(`/tasks/${id}`, {
    method: "DELETE"
  });
}

export async function fetchDueReminders(limit = 20): Promise<TaskItem[]> {
  const query = new URLSearchParams({ limit: String(limit) });
  return request<TaskItem[]>(`/tasks/reminders/due?${query.toString()}`);
}

export async function acknowledgeReminder(taskId: string): Promise<{ success: boolean }> {
  return request<{ success: boolean }>(`/tasks/${taskId}/reminders/ack`, {
    method: "POST"
  });
}
