import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from datetime import date, datetime, timedelta
from database import init_db, add_student, get_student, save_plan, get_tasks, update_task, get_summary, get_gaps
from planner import analyze_gaps, build_roadmap, make_tasks, reschedule_incomplete
from agents.skill_gap_agent import analyze_skill_gaps
from agents.roadmap_graph import run_planning_workflow
from resources import resources_for_task

st.set_page_config(page_title="CareerPilot AI", page_icon="🎯", layout="wide")
init_db()

st.title("🎯 CareerPilot AI")
st.caption("Skill-gap analysis • Personalized roadmap • Daily study planner")

with st.sidebar:
    st.header("Your profile")
    name = st.text_input("Name", value="Student")
    education = st.selectbox("Education", ["B.Tech / B.E. CSE", "Other engineering", "Science degree", "Other"])
    target_role = st.selectbox("Target career", ["Software Development Engineer", "Data Analyst", "Machine Learning Engineer"])
    known_skills_text = st.text_input("Skills you already know (comma-separated)", "Python, SQL")
    level = st.selectbox("Current level", ["Beginner", "Intermediate", "Advanced"])
    hours_per_day = st.slider("Study time per day (hours)", 0.5, 6.0, 2.0, 0.5)
    start_date = st.date_input("Start date", value=date.today())
    save_profile = st.button("Save profile", type="primary", use_container_width=True)

    if save_profile:
        known_skills = [x.strip() for x in known_skills_text.split(",") if x.strip()]
        student_id = add_student(name, education, target_role, known_skills, level, hours_per_day)
        st.session_state["student_id"] = student_id
        st.success("Profile saved.")

student_id = st.session_state.get("student_id")
if not student_id:
    st.info("Start in the sidebar: enter your profile and click **Save profile**.")
    st.markdown("""
    **How it works**
    1. Compare your current skills with a starter skill profile for your chosen career.
    2. Generate a learning roadmap and manageable study tasks.
    3. Mark tasks complete and let the planner reschedule unfinished work.

    This course-project MVP uses transparent rules and SQLite by default. It does not claim that a skill level or duration is an exact measurement.
    """)
    st.stop()

student = get_student(student_id)
if not student:
    st.error("Profile not found. Save your profile again.")
    st.stop()

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Skill gaps", "Roadmap & tasks", "Progress & reminders"])

with tab1:
    st.subheader(f"Welcome, {student['name']}")
    st.write(f"**Target role:** {student['target_role']}  ·  **Study availability:** {student['hours_per_day']} hours/day")
    summary = get_summary(student_id)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tasks", summary["total"])
    c2.metric("Completed", summary["completed"])
    c3.metric("Remaining", summary["remaining"])
    c4.metric("Completion", f"{summary['percent']}%")
    st.progress(summary["percent"] / 100 if summary["total"] else 0)
    st.markdown("#### Next steps")
    st.write("Open **Skill gaps** to inspect the analysis, then create a roadmap. Your roadmap tasks and progress are saved in the project database.")

with tab2:
    st.subheader("Skill-gap analysis")
    analysis = analyze_skill_gaps(student["target_role"], student["known_skills"], student["level"])
    gaps = analysis["gaps"]
    st.caption(f"Analysis mode: {analysis['mode']}")
    st.write(analysis["summary"])
    if gaps:
        for gap in gaps:
            with st.container(border=True):
                left, mid, right = st.columns([2, 2, 1])
                left.markdown(f"**{gap['skill']}**")
                mid.write(gap["reason"])
                right.write(f"Priority: **{gap['priority']}**")
    else:
        st.success("Your listed skills cover the starter requirements. Consider validating your proficiency with a practical assessment.")
    st.caption("Starter requirements are illustrative. Replace them with requirements collected from job descriptions for a stronger evaluation.")
    st.markdown(f"**Preferred start date:** {start_date.isoformat()}")
    st.write("First prepare a preview. Your dated to-do list will only be saved after you approve it.")
    if st.button("Prepare roadmap and to-do list preview", type="primary"):
        result = run_planning_workflow(
            student["target_role"], gaps, float(student["hours_per_day"]), start_date
        )
        st.session_state["pending_plan"] = result
        st.session_state["pending_plan_start_date"] = start_date.isoformat()
        st.session_state["pending_plan_nonce"] = st.session_state.get("pending_plan_nonce", 0) + 1

    pending_plan = st.session_state.get("pending_plan")
    if pending_plan:
        pending_tasks = pending_plan.get("tasks", [])
        st.markdown("### Review your proposed schedule")
        st.info(f"This plan contains {len(pending_tasks)} tasks and starts on {st.session_state.get('pending_plan_start_date', start_date.isoformat())}.")
        for task in pending_tasks[:5]:
            st.markdown(f"- **Day {task['day_number']} · {task['due_date']} — {task['title']}** ({task['estimated_minutes']} min)")
        if len(pending_tasks) > 5:
            st.caption(f"Plus {len(pending_tasks) - 5} more tasks. You can review the saved plan and resources in Roadmap & tasks.")
        consent_key = f"approve_todo_list_{st.session_state.get('pending_plan_nonce', 0)}"
        consent = st.checkbox("I approve creating this dated to-do list and saving it to my profile.", key=consent_key)
        if st.button("Save my approved to-do list", type="primary", disabled=(not consent or not pending_tasks)):
            save_plan(student_id, pending_plan["roadmap"], pending_tasks)
            st.session_state["workflow_notes"] = pending_plan.get("notes", [])
            del st.session_state["pending_plan"]
            st.session_state.pop("pending_plan_start_date", None)
            st.success(f"Saved {len(pending_tasks)} tasks. Learning links and video suggestions are included.")
            st.rerun()

with tab3:
    st.subheader("Roadmap and tasks")
    tasks = get_tasks(student_id)
    if not tasks:
        st.info("No saved to-do list yet. Go to Skill gaps, prepare a preview, and approve the schedule to save it.")
    else:
        grouped = {}
        for task in tasks:
            grouped.setdefault(task["day_number"], []).append(task)
        for day_number, day_tasks in grouped.items():
            due = day_tasks[0]["due_date"]
            st.markdown(f"#### Day {day_number} · {due}")
            for task in day_tasks:
                cols = st.columns([0.5, 3.4, 1, 1.2, 1])
                new_status = cols[0].checkbox("Done", value=task["status"] == "Completed", key=f"done_{task['id']}", label_visibility="collapsed")
                cols[1].markdown(f"**{task['title']}**")
                cols[1].caption(task["description"])
                cols[2].write(f"{task['estimated_minutes']} min")
                cols[3].write(task["status"])
                if new_status != (task["status"] == "Completed"):
                    update_task(task["id"], "Completed" if new_status else "Pending")
                    st.rerun()
                with st.expander("📚 Learning materials and video suggestions"):
                    task_resources = task.get("resources") or resources_for_task(task.get("skill", ""), task["title"])
                    websites = [item for item in task_resources if item.get("kind") != "YouTube video search"]
                    videos = [item for item in task_resources if item.get("kind") == "YouTube video search"]
                    if websites:
                        st.markdown("**Websites and practice materials**")
                        for item in websites:
                            st.markdown(f"- [{item['title']}]({item['url']}) — {item['kind']}")
                    if videos:
                        st.markdown("**Video suggestions**")
                        for item in videos:
                            st.markdown(f"- [{item['title']}]({item['url']})")
                    st.caption("Resources are suggested starting points. Check the content level and choose the material that fits your needs.")
        st.divider()
        if st.button("Reschedule unfinished tasks", type="primary"):
            reschedule_incomplete(student_id, date.today())
            st.success("Unfinished tasks moved into a new sequence starting today.")
            st.rerun()

with tab4:
    st.subheader("Progress and study reminders")
    tasks = get_tasks(student_id)
    today = date.today()
    due_today = [t for t in tasks if t["due_date"] == today.isoformat() and t["status"] != "Completed"]
    overdue = [t for t in tasks if t["due_date"] < today.isoformat() and t["status"] != "Completed"]
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🔔 Due today")
        if due_today:
            for t in due_today:
                st.warning(f"{t['title']} — {t['estimated_minutes']} min")
        else:
            st.success("No unfinished tasks due today.")
    with c2:
        st.markdown("#### ⏰ Overdue")
        if overdue:
            for t in overdue:
                st.warning(f"{t['title']} — was due {t['due_date']}")
        else:
            st.success("No overdue tasks.")
    st.markdown("#### Adaptive replanning")
    with st.form("adaptive_feedback"):
        score = st.slider("Latest quiz / practice score (%)", 0, 100, 75)
        missed_count = st.number_input("Tasks missed recently", min_value=0, max_value=20, value=len(overdue))
        apply_feedback = st.form_submit_button("Ask planner to adapt my plan")
    if apply_feedback:
        current_gaps = analyze_skill_gaps(
            student["target_role"], student["known_skills"], student["level"]
        )["gaps"]
        st.session_state["adapted_plan"] = run_planning_workflow(
            student["target_role"],
            current_gaps,
            float(student["hours_per_day"]),
            date.today(),
            {"assessment_score": score, "missed_tasks": int(missed_count)},
        )

    feedback_result = st.session_state.get("adapted_plan")
    if feedback_result:
        st.info(f"Planner decision: **{feedback_result.get('decision', 'continue')}**")
        for note in feedback_result.get("notes", []):
            st.write(f"• {note}")
        st.write(f"Proposed task count: {len(feedback_result.get('tasks', []))}")
        if st.button("Replace current tasks with adapted plan", key="replace_adapted_plan"):
            save_plan(student_id, feedback_result["roadmap"], feedback_result["tasks"])
            del st.session_state["adapted_plan"]
            st.success("Your plan has been updated.")
            st.rerun()
    st.caption("These reminders appear when you open the app. Background email or mobile push notifications are not included in this MVP.")
    summary = get_summary(student_id)
    st.markdown("#### Progress summary")
    st.write(f"You have completed **{summary['completed']} of {summary['total']}** tasks.")
    if summary["total"]:
        st.progress(summary["percent"] / 100)
