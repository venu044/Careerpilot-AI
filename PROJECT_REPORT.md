# CareerPilot AI — Mini Project Report

## Abstract
CareerPilot AI is a career-learning planner that compares a learner's self-reported skills with a starter set of requirements for a selected career. It identifies possible gaps, creates a topic-based learning roadmap, estimates study effort, and prepares a dated to-do list based on the learner's available time. Students preview and explicitly approve the proposed schedule before it is saved. Each saved task includes curated learning websites and a topic-specific YouTube video-search suggestion. Task completion is stored locally so the dashboard can show progress and overdue work.

## Objectives
- Identify possible gaps between a student's listed skills and a target career.
- Use Gemini to refine gap explanations and priorities when configured.
- Keep the application usable with deterministic local rules if Gemini is unavailable.
- Organize missing skills into a topic-based roadmap.
- Recommend learning materials and video searches for each scheduled task.
- Estimate effort and assign dates according to study availability.
- Ask the learner to approve the to-do list before saving it.
- Track task completion and support simple adaptive replanning.

## Modules
1. Student profile (prototype profile, not a complete account system)
2. Gemini-assisted skill-gap analysis with rule-based fallback
3. Roadmap and task generation
4. Curated learning-resource catalog
5. Schedule preview and explicit approval
6. Progress tracking, in-app reminders and rescheduling

## Methodology
The current prototype stores learner profiles and tasks in SQLite. A rule-based matching function compares normalized skill names with a starter set of requirements for the selected role. When `GEMINI_API_KEY` is configured, the Google Gen AI Python SDK sends the approved candidate gaps to Gemini for concise explanations and priority refinement. The application constrains Gemini's output to the locally approved candidates; if the key is absent or the request fails, local rules are used. Topic plans are converted into dated tasks based on daily study capacity. Each task receives curated website resources and a YouTube search link based on its skill and topic. The learner previews the schedule and must approve it before tasks are persisted.

## Technology stack
- Python
- Streamlit
- Google Gen AI Python SDK (`google-genai`)
- LangGraph
- SQLite

## Limitations
Career requirements are illustrative rather than a live job-market feed. Proficiency is self-reported unless a practical assessment is added. Duration estimates are approximate. Curated resources may change and should be checked periodically; video links open a topic-specific search rather than endorsing a particular video. Reminders only appear in the app. This starter project uses a local SQLite database and a profile-in-session workflow; it is not yet a multi-user production system with registration, authentication, PostgreSQL and row-level access controls.

## Future scope
- Add registration and authentication with secure student-specific data access.
- Migrate the database to managed PostgreSQL for multi-user deployment.
- Import and source real job descriptions and career skill taxonomies.
- Add quizzes and practical assessments to verify skill proficiency.
- Add validated career discovery for students who have not selected a target role.
- Add optional online deployment of the model and background reminders.
- Evaluate Gemini explanations and roadmap quality using a reviewed test dataset.

## Agentic AI workflow
The LangGraph workflow creates a roadmap, schedules tasks, evaluates learner feedback, and applies a simple replanning policy. A low assessment score inserts a revision task; multiple missed tasks spread work across additional days. These policies are transparent starter rules and should be evaluated with test cases before being treated as educational recommendations.
