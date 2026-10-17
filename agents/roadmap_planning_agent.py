"""Roadmap Planning Agent: converts identified skill gaps into an ordered roadmap."""
from typing import Any
from planner import build_roadmap


def run_roadmap_planning_agent(target_role: str, gaps: list[dict[str, Any]]) -> dict[str, Any]:
    roadmap = build_roadmap(target_role, gaps)
    return {
        "roadmap": roadmap,
        "agent": "Roadmap Planning Agent",
        "summary": f"Created {len(roadmap)} roadmap sections for {target_role}.",
    }
