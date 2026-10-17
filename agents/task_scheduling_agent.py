"""Task Scheduling Agent: turns roadmap sections into dated tasks with resources."""
from typing import Any
from planner import make_tasks


def run_task_scheduling_agent(
    roadmap: list[dict[str, Any]], hours_per_day: float, start_date: Any
) -> dict[str, Any]:
    tasks = make_tasks(roadmap, float(hours_per_day), start_date)
    return {
        "tasks": tasks,
        "agent": "Task Scheduling Agent",
        "summary": f"Scheduled {len(tasks)} tasks at {hours_per_day:g} study hours per day.",
    }
