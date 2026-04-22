import { Injectable, OnApplicationShutdown } from "@nestjs/common";
import { mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";

@Injectable()
export class SqliteService implements OnApplicationShutdown {
  private readonly databasePath = this.resolveDatabasePath();
  private readonly connectionInstance = this.openAndMigrate();

  get connection(): DatabaseSync {
    return this.connectionInstance;
  }

  onApplicationShutdown() {
    this.connectionInstance.close();
  }

  private resolveDatabasePath(): string {
    const configured = process.env.SQLITE_PATH ?? "./data/todolist.db";
    return resolve(process.cwd(), configured);
  }

  private openAndMigrate(): DatabaseSync {
    mkdirSync(dirname(this.databasePath), { recursive: true });

    const db = new DatabaseSync(this.databasePath);
    db.exec("PRAGMA foreign_keys = ON;");
    db.exec("PRAGMA journal_mode = WAL;");

    db.exec(`
      CREATE TABLE IF NOT EXISTS tasks (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        notes TEXT,
        due_at TEXT,
        remind_at TEXT,
        priority TEXT NOT NULL CHECK (priority IN ('low', 'medium', 'high')),
        completed INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      );

      CREATE TABLE IF NOT EXISTS reminder_acks (
        task_id TEXT PRIMARY KEY,
        triggered_at TEXT NOT NULL,
        FOREIGN KEY(task_id) REFERENCES tasks(id) ON DELETE CASCADE
      );

      CREATE INDEX IF NOT EXISTS idx_tasks_updated_at ON tasks(updated_at DESC);
      CREATE INDEX IF NOT EXISTS idx_tasks_remind_at ON tasks(remind_at);
      CREATE INDEX IF NOT EXISTS idx_tasks_completed ON tasks(completed);
    `);

    return db;
  }
}
