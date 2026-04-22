import { IsBoolean, IsIn, IsOptional, IsString, MaxLength, MinLength } from "class-validator";
import type { TaskPriority } from "../task.model";

export class UpdateTaskDto {
  @IsOptional()
  @IsString()
  @MinLength(1)
  @MaxLength(120)
  title?: string;

  @IsOptional()
  @IsString()
  @MaxLength(600)
  notes?: string;

  @IsOptional()
  @IsString()
  dueAt?: string;

  @IsOptional()
  @IsString()
  remindAt?: string;

  @IsOptional()
  @IsIn(["low", "medium", "high"])
  priority?: TaskPriority;

  @IsOptional()
  @IsBoolean()
  completed?: boolean;
}
