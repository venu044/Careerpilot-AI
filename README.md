<<<<<<< HEAD
# CareerPilot AI

CareerPilot AI is a student-friendly career-learning planner. It analyzes skill gaps, builds a roadmap, schedules study tasks, links to learning materials and video suggestions, tracks progress, and adapts the plan after feedback.

## Features

- Student profile and target-career selection
- Gemini-assisted skill-gap explanations using Google's official `google-genai` SDK
- Rule-based fallback if the Gemini key is missing, quota is exhausted, or the model is unavailable
- Curated role requirements for SDE, Data Analyst, and Machine Learning Engineer
- Roadmaps and date-based to-do lists scheduled around daily study availability
- Explicit preview and student approval before a proposed to-do list is saved
- Per-task learning resources, including documentation, interactive practice, free courses and topic-specific YouTube video searches
- Task completion tracking, progress summaries and in-app due/overdue reminders
- LangGraph workflow for roadmap generation, scheduling, feedback evaluation and adaptation
- SQLite by default for a simple local demo; database module can be extended for PostgreSQL

## Tech stack

- Python and Streamlit
- LangGraph
- Google Gen AI Python SDK (`google-genai`)
- SQLite for the starter local database

## 1. Run locally

Python 3.10+ is recommended.

### Windows

```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
streamlit run app.py
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

The app can run without Gemini by using the local rule-based skill-gap analyzer. Add a Gemini key to enable LLM-assisted explanations.

## 2. Configure Gemini

1. Obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Put the following values in `.env`:

```dotenv
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.8-flash
```

3. Restart Streamlit after saving the file.

The implementation uses `from google import genai`, `genai.Client(...)`, and `client.models.generate_content(...)` from the official Google Gen AI SDK. Choose a model ID available to your Google AI Studio project; if the configured model is unavailable or rate-limited, the application falls back to rule-based analysis. API access can have quotas or billing requirements depending on your account and model; a key does not guarantee unlimited usage.

**Security:** do not commit `.env` or publish your API key. For Streamlit Community Cloud, configure `GEMINI_API_KEY` and `GEMINI_MODEL` in the app's Secrets settings instead of uploading `.env`.

## 3. How the learning resources work

Each generated task is enriched with curated learning resources selected from `resources.py`. Examples include official documentation, interactive exercises and free learning courses. The video suggestion opens a topic-specific YouTube search, rather than claiming that one specific video is always current or suitable.

The resource catalog is intentionally separate from Gemini. This prevents the model from inventing URLs. Review and expand `RESOURCE_CATALOG` as you add careers and skills. Always check that resources remain available and match the learner's level.

## 4. How the to-do approval works

1. Save the student profile and inspect the skill-gap analysis.
2. Select the preferred start date in the sidebar.
3. Click **Prepare roadmap and to-do list preview**.
4. Review the proposed schedule and check the approval box.
5. Click **Save my approved to-do list**.
6. Open **Roadmap & tasks** to mark tasks complete and expand each task's learning materials.

The schedule uses estimated learning effort and the student's daily available study time. These are estimates, not guarantees. Reminders appear when the app is open; background email or push notifications are not implemented.

## 5. Suggested demo

1. Select `Software Development Engineer`.
2. Enter skills such as `Python, SQL` and choose a level.
3. Set daily study availability and a preferred start date.
4. Open **Skill gaps** and inspect the analysis mode (Gemini-assisted or rule-based fallback).
5. Prepare a roadmap preview and explicitly approve the dated to-do list.
6. Open **Roadmap & tasks** and expand a task to see documentation, practice websites and a YouTube video search suggestion.
7. Mark a task complete and view the progress dashboard.
8. Try adaptive replanning with a low assessment score or several missed tasks.

## 6. Tests

```bash
python -m unittest discover -s tests -v
```

The tests use local logic and do not require a Gemini API key or network access.

## Limitations

- Starter career requirements are illustrative and should be validated against real job descriptions.
- Skill proficiency is self-reported unless the app collects assessment evidence.
- Gemini output is constrained to the locally approved gap candidates, but it still needs evaluation.
- Curated resource links may change; verify them periodically.
- YouTube links are searches for topic-specific videos, not endorsements of every search result.
- SQLite is suitable for a local prototype. A multi-student public deployment should use a managed database and proper authentication/authorization before handling real student data.
- Gemini API quotas can be exhausted. Rule-based analysis remains available as a fallback.

## Main modules

- `app.py`: Streamlit UI, profile, preview/approval flow, task resources and progress views.
- `agents/skill_gap_agent.py`: Gemini integration and safe rule-based fallback.
- `agents/roadmap_graph.py`: LangGraph planning and adaptation workflow.
- `planner.py`: role requirements, gap matching and task scheduling.
- `resources.py`: curated websites and video search suggestions.
- `database.py`: SQLite persistence and backward-compatible task-resource migration.
- `tests/`: offline unit tests.
=======
# Careerpilot-AI
CareerPilot AI is an AI-powered career guidance platform that analyzes students' skills, identifies skill gaps, recommends suitable career paths, and generates personalized learning roadmaps. Built with Python, Streamlit and LangGraph, adaptive task scheduling, progress monitoring, and curated learning resources and video suggestions.
>>>>>>> 6c74ec382b5446fe275727946006eebf4d29f567
