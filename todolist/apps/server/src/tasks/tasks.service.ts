import { Injectable, NotFoundException } from "@nestjs/common";
import { randomUUID } from "node:crypto";
import { DatabaseSync } from "node:sqlite";
import { SqliteService } from "../database/sqlite.service";
import { CreateTaskDto } from "./dto/create-task.dto";
import { UpdateTaskDto } from "./dto/update-task.dto";
import { TaskModel } from "./task.model";

interface TaskRow {
  id: string;
  title: string;
  notes: string | null;
  due_at: string | null;
  remind_at: string | null;
  reminder_acknowledged_at: string | null;
  priority: "low" | "medium" | "high";
  completed: number;
  created_at: string;
  updated_at: string;
}

@Injectable()
export class TasksService {
  private readonly db: DatabaseSync;

  constructor(sqliteService: SqliteService) {
    this.db = sqliteService.connection;
  }

  list(): TaskModel[] {
    const rows = this.db
      .prepare(
        `
          SELECT
            t.id,
            t.title,
            t.notes,
            t.due_at,
            t.remind_at,
            t.priority,
            t.completed,
            t.created_at,
            t.updated_at,
            ra.triggered_at AS reminder_acknowledged_at
          FROM tasks t
          LEFT JOIN reminder_acks ra ON ra.task_id = t.id
          ORDER BY t.updated_at DESC
        `
      )
      .all() as unknown as TaskRow[];

    return rows.map((row) => this.mapRowToTask(row));
  }

  create(dto: CreateTaskDto): TaskModel {
    const now = new Date().toISOString();
    const id = randomUUID();
    const normalizedDueAt = this.normalizeDateInput(dto.dueAt);
    const normalizedRemindAt = this.normalizeDateInput(dto.remindAt);

    this.db
      .prepare(
        `
          INSERT INTO tasks (
            id,
            title,
            notes,
            due_at,
            remind_at,
            priority,
            completed,
            created_at,
            updated_at
          ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        `
      )
      .run(
        id,
        dto.title,
        dto.notes ?? null,
        normalizedDueAt ?? null,
        normalizedRemindAt ?? null,
        dto.priority,
        0,
        now,
        now
      );

    return this.getByIdOrThrow(id);
  }

  update(id: string, dto: UpdateTaskDto): TaskModel {
    const current = this.getByIdOrThrow(id);
    const now = new Date().toISOString();
    const normalizedDueAt = dto.dueAt === undefined ? current.dueAt : this.normalizeDateInput(dto.dueAt);
    const normalizedRemindAt = dto.remindAt === undefined ? current.remindAt : this.normalizeDateInput(dto.remindAt);

    const next: TaskModel = {
      ...current,
      ...dto,
      dueAt: normalizedDueAt,
      remindAt: normalizedRemindAt,
      updatedAt: now
    };

    this.db
      .prepare(
        `
          UPDATE tasks
          SET title = ?, notes = ?, due_at = ?, remind_at = ?, priority = ?, completed = ?, updated_at = ?
          WHERE id = ?
        `
      )
      .run(
        next.title,
        next.notes ?? null,
        next.dueAt ?? null,
        next.remindAt ?? null,
        next.priority,
        next.completed ? 1 : 0,
        next.updatedAt,
        id
      );

    this.syncReminderAckState(current, next);
    return this.getByIdOrThrow(id);
  }

  toggle(id: string): TaskModel {
    const current = this.getByIdOrThrow(id);
    const toggledCompleted = !current.completed;
    const now = new Date().toISOString();

    this.db
      .prepare(`UPDATE tasks SET completed = ?, updated_at = ? WHERE id = ?`)
      .run(toggledCompleted ? 1 : 0, now, id);

    this.db.prepare(`DELETE FROM reminder_acks WHERE task_id = ?`).run(id);

    return this.getByIdOrThrow(id);
  }

  delete(id: string): { success: boolean } {
    const result = this.db.prepare(`DELETE FROM tasks WHERE id = ?`).run(id);
    if (result.changes === 0) {
      throw new NotFoundException("Task not found");
    }

    return { success: true };
  }

  listDueReminders(beforeIso?: string, limit?: number): TaskModel[] {
    const before = this.resolveBeforeIso(beforeIso);
    const safeLimit = this.resolveLimit(limit);

    const rows = this.db
      .prepare(
        `
          SELECT
            t.id,
            t.title,
            t.notes,
            t.due_at,
            t.remind_at,
            t.priority,
            t.completed,
            t.created_at,
            t.updated_at,
            ra.triggered_at AS reminder_acknowledged_at
          FROM tasks t
          LEFT JOIN reminder_acks ra ON ra.task_id = t.id
          WHERE
            t.remind_at IS NOT NULL
            AND datetime(t.remind_at) <= datetime(?)
            AND t.completed = 0
            AND ra.task_id IS NULL
          ORDER BY t.remind_at ASC
          LIMIT ?
        `
      )
      .all(before, safeLimit) as unknown as TaskRow[];

    return rows.map((row) => this.mapRowToTask(row));
  }

  acknowledgeReminder(taskId: string): { success: boolean } {
    this.getByIdOrThrow(taskId);

    this.db
      .prepare(
        `
          INSERT INTO reminder_acks (task_id, triggered_at)
          VALUES (?, ?)
          ON CONFLICT(task_id) DO UPDATE SET triggered_at = excluded.triggered_at
        `
      )
      .run(taskId, new Date().toISOString());

    return { success: true };
  }

  private getByIdOrThrow(id: string): TaskModel {
    const row = this.db
      .prepare(
        `
          SELECT
            t.id,
            t.title,
            t.notes,
            t.due_at,
            t.remind_at,
            t.priority,
            t.completed,
            t.created_at,
            t.updated_at,
            ra.triggered_at AS reminder_acknowledged_at
          FROM tasks t
          LEFT JOIN reminder_acks ra ON ra.task_id = t.id
          WHERE t.id = ?
        `
      )
      .get(id) as TaskRow | undefined;

    if (!row) {
      throw new NotFoundException("Task not found");
    }

    return this.mapRowToTask(row);
  }

  private mapRowToTask(row: TaskRow): TaskModel {
    return {
      id: row.id,
      title: row.title,
      notes: row.notes ?? undefined,
      dueAt: row.due_at ?? undefined,
      remindAt: row.remind_at ?? undefined,
      reminderAcknowledgedAt: row.reminder_acknowledged_at ?? undefined,
      priority: row.priority,
      completed: row.completed === 1,
      createdAt: row.created_at,
      updatedAt: row.updated_at
    };
  }

  private resolveBeforeIso(beforeIso?: string): string {
    if (!beforeIso) {
      return new Date().toISOString();
    }

    const parsed = new Date(beforeIso);
    if (Number.isNaN(parsed.getTime())) {
      return new Date().toISOString();
    }

    return parsed.toISOString();
  }

  private resolveLimit(limit?: number): number {
    if (!limit || Number.isNaN(limit)) {
      return 20;
    }
    return Math.max(1, Math.min(100, Math.floor(limit)));
  }

  private syncReminderAckState(previous: TaskModel, next: TaskModel) {
    if (!next.remindAt || next.completed) {
      this.db.prepare(`DELETE FROM reminder_acks WHERE task_id = ?`).run(next.id);
      return;
    }

    if (previous.remindAt !== next.remindAt) {
      this.db.prepare(`DELETE FROM reminder_acks WHERE task_id = ?`).run(next.id);
    }
  }

  private normalizeDateInput(value?: string): string | undefined {
    if (!value) {
      return undefined;
    }

    const parsed = new Date(value);
    if (Number.isNaN(parsed.getTime())) {
      return value;
    }

    return parsed.toISOString();
  }
}
