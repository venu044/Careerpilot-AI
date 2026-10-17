import os
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

from agents.skill_gap_agent import analyze_skill_gaps
from database import add_student, get_tasks, init_db, save_plan
from planner import analyze_gaps, build_roadmap, make_tasks
from resources import resources_for_task
import database


class ResourceTests(unittest.TestCase):
    def test_tasks_include_websites_and_video_suggestion(self):
        gaps = analyze_gaps("Software Development Engineer", ["Python"], "Intermediate")
        roadmap = build_roadmap("Software Development Engineer", gaps)
        tasks = make_tasks(roadmap, 2, date(2026, 10, 20))
        self.assertTrue(tasks)
        for task in tasks:
            self.assertTrue(task["resources"])
            self.assertTrue(any(r["kind"] == "YouTube video search" for r in task["resources"]))
            self.assertTrue(any(r["url"].startswith("https://") for r in task["resources"]))

    def test_unknown_skill_has_general_resources(self):
        resources = resources_for_task("An unfamiliar skill", "fundamentals")
        self.assertGreaterEqual(len(resources), 2)
        self.assertTrue(all(item["url"].startswith("https://") for item in resources))


class GeminiFallbackTests(unittest.TestCase):
    def test_missing_gemini_key_uses_rule_based_fallback(self):
        with patch.dict(os.environ, {}, clear=True):
            result = analyze_skill_gaps("Data Analyst", ["SQL"], "Beginner")
        self.assertEqual(result["mode"], "rule-based fallback")
        self.assertTrue(result["gaps"])
        self.assertIn("GEMINI_API_KEY", result["summary"])


class DatabaseResourceTests(unittest.TestCase):
    def test_resources_are_saved_and_loaded(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch.object(database, "DB_PATH", Path(temp_dir) / "test.db"):
                init_db()
                student_id = add_student("Test Student", "Other", "Data Analyst", ["SQL"], "Beginner", 1)
                task = {
                    "day_number": 1,
                    "title": "SQL basics",
                    "description": "Practice queries",
                    "estimated_minutes": 60,
                    "due_date": "2026-10-20",
                    "skill": "SQL and Databases",
                    "resources": resources_for_task("SQL and Databases", "SQL basics"),
                }
                save_plan(student_id, [], [task])
                saved = get_tasks(student_id)
                self.assertEqual(len(saved), 1)
                self.assertEqual(saved[0]["resources"], task["resources"])

    def test_existing_tasks_table_gets_resources_column(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "legacy.db"
            import sqlite3
            conn = sqlite3.connect(db_path)
            conn.execute("""CREATE TABLE students (
                id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, education TEXT NOT NULL,
                target_role TEXT NOT NULL, known_skills TEXT NOT NULL, level TEXT NOT NULL,
                hours_per_day REAL NOT NULL, created_at TEXT NOT NULL)""")
            conn.execute("""CREATE TABLE tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER NOT NULL, day_number INTEGER NOT NULL,
                title TEXT NOT NULL, description TEXT NOT NULL, estimated_minutes INTEGER NOT NULL,
                due_date TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'Pending', skill TEXT NOT NULL)""")
            conn.commit()
            conn.close()
            with patch.object(database, "DB_PATH", db_path):
                init_db()
                conn = sqlite3.connect(db_path)
                columns = {row[1] for row in conn.execute("PRAGMA table_info(tasks)")}
                conn.close()
                self.assertIn("resources", columns)


if __name__ == "__main__":
    unittest.main()
