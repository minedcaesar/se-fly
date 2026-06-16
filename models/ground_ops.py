## @file ground_ops.py
#  @brief Ground operations domain: operation plans, tasks, subtasks.

from abc import ABC
from datetime import datetime
from models.enums import PlanStatus, TaskStatus


## @brief A plan of tasks for turning a flight around on the ground.
class OperationPlan:

    ## @brief Build a plan.
    #  @param plan_id  Unique identifier.
    #  @param status   Initial PlanStatus.
    def __init__(self, plan_id: str, status: PlanStatus = PlanStatus.DRAFT):
        self._planId = plan_id
        self._status = status
        self._tasks = []

    ## @brief Move the plan back to DRAFT.
    def draft(self):
        raise NotImplementedError

    ## @brief Persist the plan as SAVED.
    def save(self):
        raise NotImplementedError


## @brief Base class for a unit of ground work.
class Task(ABC):

    ## @brief Build a task.
    #  @param task_id    Unique identifier.
    #  @param name       Human-readable name.
    #  @param start_time Planned start.
    #  @param end_time   Planned end.
    #  @param status     Initial TaskStatus.
    def __init__(self, task_id: str, name: str, start_time: datetime,
                 end_time: datetime, status: TaskStatus = TaskStatus.PENDING):
        self._taskId = task_id
        self._name = name
        self._startTime = start_time
        self._endTime = end_time
        self._status = status


## @brief A task made of ordered subtasks (e.g. a full aircraft turnaround).
class TurnaroundTask(Task):

    ## @brief Build a turnaround task (adds an empty subtask list).
    def __init__(self, task_id, name, start_time, end_time):
        super().__init__(task_id, name, start_time, end_time)
        self._subtasks = []


## @brief A simple, single-step task.
class StandardTask(Task):

    ## @brief Build a standard task.
    def __init__(self, task_id, name, start_time, end_time):
        super().__init__(task_id, name, start_time, end_time)


## @brief A single step inside a TurnaroundTask.
class Subtask:

    ## @brief Build a subtask.
    #  @param subtask_id   Unique identifier.
    #  @param name         Step name.
    #  @param is_completed Whether the step is done.
    def __init__(self, subtask_id: str, name: str, is_completed: bool = False):
        self._subtaskId = subtask_id
        self._name = name
        self._isCompleted = is_completed