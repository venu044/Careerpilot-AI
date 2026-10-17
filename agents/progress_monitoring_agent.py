"""Progress Monitoring Agent: evaluates feedback and adapts scheduled tasks."""
from datetime import timedelta
from typing import Any
from resources import resources_for_task


def evaluate_progress(feedback: dict[str, Any]) -> dict[str, Any]:
    score = feedback.get("assessment_score")
    missed = int(feedback.get("missed_tasks", 0) or 0)
    if score is not None and float(score) < 60:
        return {"decision": "add_practice", "agent": "Progress Monitoring Agent",
                "note": "Assessment score is below 60%; add targeted practice before moving on."}
    if missed >= 2:
        return {"decision": "reduce_load", "agent": "Progress Monitoring Agent",
                "note": "Several tasks were missed; spread the remaining work over more days."}
    return {"decision": "continue", "agent": "Progress Monitoring Agent",
            "note": "Progress looks on track; continue with the current plan."}


def adapt_tasks(tasks: list[dict[str, Any]], decision: str, start_date: Any) -> list[dict[str, Any]]:
    updated = [dict(task) for task in tasks]
    if decision == "add_practice":
        updated.insert(0, {
            "day_number": 1,
            "title": "Targeted revision and practice",
            "description": "Review the weakest topic, solve two practice questions, and explain the answers.",
            "estimated_minutes": 45,
            "due_date": start_date.isoformat(),
            "skill": "Revision",
            "resources": resources_for_task("Data Structures and Algorithms", "targeted revision and practice"),
        })
        for task in updated[1:]:
            task["day_number"] = int(task.get("day_number", 1)) + 1
            task["due_date"] = (start_date + timedelta(days=task["day_number"] - 1)).isoformat()
    elif decision == "reduce_load":
        for index, task in enumerate(updated):
            task["day_number"] = index + 1
            task["due_date"] = (start_date + timedelta(days=index)).isoformat()
    return updated
