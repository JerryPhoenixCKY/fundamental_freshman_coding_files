# Desktop TodoList Monorepo

This folder contains the first implementation baseline for a desktop-oriented todo product:

- desktop app shell: Tauri-ready frontend in apps/desktop
- cloud backend skeleton: NestJS API in apps/server

## Prerequisites

- Node.js 20+
- npm 10+
- Rust toolchain (required later for real Tauri builds)

## Quick start

From this directory:

1. Install dependencies
   npm install
2. Run backend
   npm run dev:server
3. Run desktop frontend web shell
   npm run dev:desktop

4. Run desktop + backend together
   npm run dev

## Configuration

- Full setup guide: [CONFIGURATION.md](CONFIGURATION.md)
- Local editable env files: [apps/desktop/.env](apps/desktop/.env), [apps/server/.env](apps/server/.env)
- Env templates for sharing: [apps/desktop/.env.example](apps/desktop/.env.example), [apps/server/.env.example](apps/server/.env.example)

## Current scope

- local task list UI with quick add, schedule fields, and clock panel
- desktop reminder polling with browser notifications + sound + dismiss UI
- backend APIs for health, auth code flow, task CRUD, due reminder query, and reminder acknowledge
- SQLite persistence for tasks/reminder acknowledgements (configured via SQLITE_PATH)
- Tauri Rust scaffold files prepared, pending local Rust installation
