"""LangGraph orchestration for the four CareerPilot AI specialist agents."""
from typing import TypedDict, Any
from agents.roadmap_planning_agent import run_roadmap_planning_agent
from agents.task_scheduling_agent import run_task_scheduling_agent
from agents.progress_monitoring_agent import evaluate_progress, adapt_tasks


class PlannerState(TypedDict, total=False):
    target_role: str
    gaps: list[dict[str, Any]]
    hours_per_day: float
    start_date: Any
    roadmap: list[dict[str, Any]]
    tasks: list[dict[str, Any]]
    feedback: dict[str, Any]
    decision: str
    notes: list[str]
    agent_trace: list[str]


def _create_roadmap(state: PlannerState) -> PlannerState:
    result = run_roadmap_planning_agent(state["target_role"], state.get("gaps", []))
    return {
        "roadmap": result["roadmap"],
        "notes": state.get("notes", []) + [result["summary"]],
        "agent_trace": state.get("agent_trace", []) + [result["agent"]],
    }


def _schedule_tasks(state: PlannerState) -> PlannerState:
    result = run_task_scheduling_agent(
        state.get("roadmap", []), state.get("hours_per_day", 2.0), state["start_date"]
    )
    return {
        "tasks": result["tasks"],
        "notes": state.get("notes", []) + [result["summary"]],
        "agent_trace": state.get("agent_trace", []) + [result["agent"]],
    }


def _evaluate_feedback(state: PlannerState) -> PlannerState:
    result = evaluate_progress(state.get("feedback", {}))
    return {
        "decision": result["decision"],
        "notes": state.get("notes", []) + [result["note"]],
        "agent_trace": state.get("agent_trace", []) + [result["agent"]],
    }


def _adapt_tasks(state: PlannerState) -> PlannerState:
    tasks = adapt_tasks(state.get("tasks", []), state.get("decision", "continue"), state["start_date"])
    return {
        "tasks": tasks,
        "notes": state.get("notes", []) + ["Progress Monitoring Agent applied the selected adaptation."],
    }


def build_planning_graph():
    try:
        from langgraph.graph import StateGraph, END
    except ImportError as exc:
        raise RuntimeError("LangGraph is not installed. Run: pip install -r requirements.txt") from exc
    graph = StateGraph(PlannerState)
    graph.add_node("roadmap_planning_agent", _create_roadmap)
    graph.add_node("task_scheduling_agent", _schedule_tasks)
    graph.add_node("progress_monitoring_agent", _evaluate_feedback)
    graph.add_node("apply_adaptation", _adapt_tasks)
    graph.set_entry_point("roadmap_planning_agent")
    graph.add_edge("roadmap_planning_agent", "task_scheduling_agent")
    graph.add_edge("task_scheduling_agent", "progress_monitoring_agent")
    graph.add_edge("progress_monitoring_agent", "apply_adaptation")
    graph.add_edge("apply_adaptation", END)
    return graph.compile()


def run_planning_workflow(target_role, gaps, hours_per_day, start_date, feedback=None):
    """Run roadmap planning, scheduling, and feedback adaptation agents."""
    return build_planning_graph().invoke({
        "target_role": target_role,
        "gaps": gaps,
        "hours_per_day": float(hours_per_day),
        "start_date": start_date,
        "feedback": feedback or {},
        "notes": [],
        "agent_trace": [],
    })
