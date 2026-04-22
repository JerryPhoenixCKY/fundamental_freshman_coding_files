import { Module } from "@nestjs/common";
import { AuthModule } from "./auth/auth.module";
import { DatabaseModule } from "./database/database.module";
import { HealthModule } from "./health/health.module";
import { TasksModule } from "./tasks/tasks.module";

@Module({
  imports: [DatabaseModule, HealthModule, AuthModule, TasksModule]
})
export class AppModule {}
