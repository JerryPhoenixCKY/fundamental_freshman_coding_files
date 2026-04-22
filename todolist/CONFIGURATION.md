# Configuration Guide

This document separates configuration into two groups:

- Completed automatically in code
- Requires your local machine setup

## 1) Already configured in project

### Monorepo scripts

Configured in [package.json](package.json):

- dev: run backend and desktop web shell together
- dev:server / dev:desktop: run each app separately
- check: compile both apps

### Desktop runtime env

Configured in [apps/desktop/vite.config.ts](apps/desktop/vite.config.ts) and [apps/desktop/.env.example](apps/desktop/.env.example):

- VITE_PORT controls desktop web shell dev port
- VITE_API_BASE controls backend API base URL
- VITE_REMINDER_POLL_MS controls reminder polling interval in milliseconds
- VITE_REMINDER_SOUND controls reminder beep enablement

Default local file has been created at [apps/desktop/.env](apps/desktop/.env).

### Server runtime env

Configured in [apps/server/src/main.ts](apps/server/src/main.ts), [apps/server/src/auth/auth.service.ts](apps/server/src/auth/auth.service.ts), and [apps/server/.env.example](apps/server/.env.example):

- PORT controls server listen port
- API_PREFIX controls global route prefix
- CORS_ORIGIN controls allowed desktop origins (comma-separated)
- AUTH_CODE_EXPIRES_SECONDS controls email code validity
- SQLITE_PATH controls local SQLite file path

Default local file has been created at [apps/server/.env](apps/server/.env).

### Local env ignore policy

Configured in [.gitignore](.gitignore):

- .env and .env.* are ignored
- .env.example remains tracked

## 2) You need to configure manually

### Rust toolchain (required for real Tauri desktop app)

Current machine is missing rustc and cargo.

PowerShell commands:

1. Install rustup
   winget install Rustlang.Rustup --accept-source-agreements --accept-package-agreements
2. Reload terminal and verify
   rustc -V
   cargo -V

If winget is unavailable, use installer from:
<https://rustup.rs/>

### Tauri Windows prerequisites

1. Install Microsoft C++ Build Tools if missing
   winget install Microsoft.VisualStudio.2022.BuildTools --accept-source-agreements --accept-package-agreements
2. Ensure WebView2 Runtime is present (usually preinstalled on Windows 10/11)
   winget install Microsoft.EdgeWebView2Runtime --accept-source-agreements --accept-package-agreements

### Production signing (later release stage)

You need a code-signing certificate and private key for production builds. This cannot be auto-configured safely in repository.

## 3) How to run after configuration

From [todolist](.):

1. Install dependencies
   npm install
2. Start both services
   npm run dev
3. Validate backend health
   <http://localhost:3000/api/health>

## 4) Optional customizations

- If you change server PORT or API_PREFIX, update desktop VITE_API_BASE accordingly.
- For multiple frontend origins, set CORS_ORIGIN as comma-separated list.
