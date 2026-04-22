import { Body, Controller, Delete, Get, Param, Patch, Post, Query } from "@nestjs/common";
import { CreateTaskDto } from "./dto/create-task.dto";
import { UpdateTaskDto } from "./dto/update-task.dto";
import { TasksService } from "./tasks.service";

@Controller("tasks")
export class TasksController {
  constructor(private readonly tasksService: TasksService) {}

  @Get()
  list() {
    return this.tasksService.list();
  }

  @Get("reminders/due")
  listDueReminders(@Query("before") before?: string, @Query("limit") limit?: string) {
    const parsedLimit = Number(limit);
    return this.tasksService.listDueReminders(before, Number.isFinite(parsedLimit) ? parsedLimit : undefined);
  }

  @Post()
  create(@Body() dto: CreateTaskDto) {
    return this.tasksService.create(dto);
  }

  @Patch(":id")
  update(@Param("id") id: string, @Body() dto: UpdateTaskDto) {
    return this.tasksService.update(id, dto);
  }

  @Patch(":id/toggle")
  toggle(@Param("id") id: string) {
    return this.tasksService.toggle(id);
  }

  @Post(":id/reminders/ack")
  acknowledgeReminder(@Param("id") id: string) {
    return this.tasksService.acknowledgeReminder(id);
  }

  @Delete(":id")
  delete(@Param("id") id: string) {
    return this.tasksService.delete(id);
  }
}
