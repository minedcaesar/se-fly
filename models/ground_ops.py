from abc import ABC
from datetime import datetime
from models.enums import PlanStatus, TaskStatus


class OperationPlan:
    def __init__(self, plan_id: str, status: PlanStatus = PlanStatus.DRAFT):
        self._planId = plan_id
        self._status = status
        self._tasks = []

    def draft(self):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError


class Task(ABC):
    def __init__(self, task_id: str, name: str, start_time: datetime,
                 end_time: datetime, status: TaskStatus = TaskStatus.PENDING):
        self._taskId = task_id
        self._name = name
        self._startTime = start_time
        self._endTime = end_time
        self._status = status


class TurnaroundTask(Task):
    def __init__(self, task_id, name, start_time, end_time):
        super().__init__(task_id, name, start_time, end_time)
        self._subtasks = []


class StandardTask(Task):
    def __init__(self, task_id, name, start_time, end_time):
        super().__init__(task_id, name, start_time, end_time)


class Subtask:
    def __init__(self, subtask_id: str, name: str, is_completed: bool = False):
        self._subtaskId = subtask_id
        self._name = name
        self._isCompleted = is_completed
