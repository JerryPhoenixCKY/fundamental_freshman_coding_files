export type TaskPriority = "low" | "medium" | "high";

export interface TaskItem {
  id: string;
  title: string;
  notes?: string;
  dueAt?: string;
  remindAt?: string;
  reminderAcknowledgedAt?: string;
  priority: TaskPriority;
  completed: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface CreateTaskInput {
  title: string;
  notes?: string;
  dueAt?: string;
  remindAt?: string;
  priority: TaskPriority;
}
