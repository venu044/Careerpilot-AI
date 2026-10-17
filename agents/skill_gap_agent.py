"""Gemini-assisted skill-gap analysis with a deterministic fallback."""
import json
import os
from typing import Any

from planner import analyze_gaps


def analyze_skill_gaps(target_role: str, known_skills: list[str], level: str) -> dict[str, Any]:
    """Return structured gaps using Gemini when configured, otherwise local rules.

    Gemini may refine the priority and explanation of known gap candidates, but it
    cannot introduce skills outside the application's curated role requirements.
    """
    fallback = analyze_gaps(target_role, known_skills, level)
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return {
            "mode": "rule-based fallback",
            "summary": "GEMINI_API_KEY is not configured, so the local skill rules were used.",
            "gaps": fallback,
        }

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        prompt = {
            "target_role": target_role,
            "known_skills": known_skills,
            "self_reported_level": level,
            "approved_gap_candidates": fallback,
            "instructions": (
                "Analyze career-learning skill gaps. Treat skills as self-reported, not verified. "
                "Only return items from approved_gap_candidates; do not invent additional skills. "
                "Return valid JSON with keys summary and gaps. Each gap must have skill, priority "
                "(High/Medium/Low), reason, current_level, required_level. Do not invent job-market "
                "statistics, guarantees, or certifications. Keep explanations actionable and concise."
            ),
        }
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip(),
            contents=json.dumps(prompt, ensure_ascii=False),
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are a careful career-learning assistant. Return only valid JSON. "
                    "Never add skills not present in the approved candidates."
                ),
                response_mime_type="application/json",
                temperature=0.2,
                max_output_tokens=2500,
            ),
        )
        data = json.loads(response.text or "{}")
        raw_gaps = data.get("gaps", fallback)
        if not isinstance(raw_gaps, list):
            raw_gaps = fallback

        allowed = {str(item["skill"]).strip().casefold(): item for item in fallback}
        allowed_priorities = {"High", "Medium", "Low"}
        clean_gaps = []
        seen = set()
        for item in raw_gaps:
            if not isinstance(item, dict) or not item.get("skill"):
                continue
            key = str(item["skill"]).strip().casefold()
            if key not in allowed or key in seen:
                continue
            seen.add(key)
            original = allowed[key]
            priority = item.get("priority", original["priority"])
            if priority not in allowed_priorities:
                priority = original["priority"]
            clean_gaps.append({
                "skill": original["skill"],
                "priority": priority,
                "reason": str(item.get("reason", original["reason"]))[:500],
                "current_level": str(item.get("current_level", original["current_level"]))[:100],
                "required_level": str(item.get("required_level", original["required_level"]))[:100],
            })

        # Preserve any approved candidates the model omitted; Gemini refines rather
        # than silently removes the locally identified skill gaps.
        included = {item["skill"].casefold() for item in clean_gaps}
        clean_gaps.extend(item for item in fallback if item["skill"].casefold() not in included)
        return {
            "mode": "Gemini-assisted" if clean_gaps or not fallback else "rule-based fallback",
            "summary": str(data.get("summary", "Skill-gap analysis prepared with Gemini assistance."))[:1000],
            "gaps": clean_gaps,
        }
    except Exception as exc:
        # Quota, network, model-name and response errors should not break the app.
        return {
            "mode": "rule-based fallback",
            "summary": f"Gemini was unavailable; local skill rules were used ({type(exc).__name__}).",
            "gaps": fallback,
        }
