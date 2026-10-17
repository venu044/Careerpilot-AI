import unittest
from datetime import date
from planner import analyze_gaps, build_roadmap, make_tasks

class PlannerTests(unittest.TestCase):
    def test_gap_analysis_finds_missing_skills(self):
        gaps = analyze_gaps("Software Development Engineer", ["Python", "SQL"], "Intermediate")
        names = {item["skill"] for item in gaps}
        self.assertIn("Data Structures and Algorithms", names)
        self.assertIn("Git and GitHub", names)

    def test_tasks_have_dates_and_effort(self):
        gaps = analyze_gaps("Data Analyst", ["SQL"], "Intermediate")
        roadmap = build_roadmap("Data Analyst", gaps)
        tasks = make_tasks(roadmap, 2, date(2026, 1, 1))
        self.assertTrue(tasks)
        self.assertTrue(all(task["estimated_minutes"] > 0 for task in tasks))
        self.assertTrue(all(task["due_date"] for task in tasks))

if __name__ == "__main__":
    unittest.main()
