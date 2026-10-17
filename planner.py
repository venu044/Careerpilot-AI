from datetime import timedelta
from resources import resources_for_task

# Starter skill profiles. For a real deployment, maintain these from verified job descriptions.
CAREER_REQUIREMENTS = {
    "Software Development Engineer": [
        ("Data Structures and Algorithms", "High", "Important for coding interviews and problem solving."),
        ("Object-Oriented Programming", "High", "Useful for designing maintainable applications."),
        ("SQL and Databases", "Medium", "Needed to store and query application data."),
        ("Git and GitHub", "Medium", "Used for version control and collaboration."),
        ("REST APIs", "Medium", "Useful for connecting frontends and backend services."),
        ("Backend Development", "High", "Builds the services that power applications."),
        ("System Design Basics", "Medium", "Helps explain how software components fit together."),
    ],
    "Data Analyst": [
        ("SQL and Databases", "High", "Frequently used to retrieve and transform business data."),
        ("Python for Data Analysis", "High", "Useful for cleaning and analyzing datasets."),
        ("Statistics", "High", "Supports sound interpretation of data."),
        ("Data Visualization", "Medium", "Communicates findings clearly."),
        ("Excel or Spreadsheets", "Medium", "Commonly used for analysis and reporting."),
        ("Dashboard Projects", "Medium", "Demonstrates end-to-end analytical work."),
    ],
    "Machine Learning Engineer": [
        ("Python for Data Science", "High", "Core language for many ML workflows."),
        ("Statistics and Linear Algebra", "High", "Supports understanding of model behavior."),
        ("Data Cleaning and Feature Engineering", "High", "Improves the quality of model inputs."),
        ("Machine Learning Algorithms", "High", "Core knowledge for building models."),
        ("Model Evaluation", "High", "Helps measure generalization and avoid misleading results."),
        ("APIs and Model Deployment", "Medium", "Makes models usable by other applications."),
    ],
}

TOPIC_PLANS = {
    "Data Structures and Algorithms": [
        ("Arrays and Strings", 90, "Review common operations, then solve 2–3 practice problems."),
        ("Hashing and Two Pointers", 100, "Learn patterns and solve problems with a written explanation."),
        ("Binary Search", 90, "Practice search on sorted data and boundary cases."),
        ("Linked Lists, Stacks and Queues", 120, "Implement each structure and solve a few exercises."),
        ("Trees and Graph Basics", 150, "Study traversals and solve introductory problems."),
    ],
    "Object-Oriented Programming": [
        ("Classes and Objects", 60, "Create small classes and practice constructors and methods."),
        ("Inheritance and Polymorphism", 75, "Write examples and explain when each concept is useful."),
        ("Interfaces and Design Practice", 75, "Model a small real-world problem using OOP."),
    ],
    "SQL and Databases": [
        ("SELECT, WHERE and ORDER BY", 60, "Practice filtering and sorting rows."),
        ("JOINs and Aggregations", 90, "Solve queries involving multiple tables and GROUP BY."),
        ("Keys and Database Design", 75, "Design a small schema with primary and foreign keys."),
    ],
    "Git and GitHub": [
        ("Git Basics", 45, "Practice init, status, add, commit and log."),
        ("Branches and Remote Repositories", 60, "Create a branch and push a small repository."),
    ],
    "REST APIs": [
        ("HTTP and REST Basics", 60, "Understand methods, status codes and JSON."),
        ("Build a Small API", 90, "Create a few endpoints and test them."),
    ],
    "Backend Development": [
        ("Backend Request Flow", 60, "Understand routes, validation and service logic."),
        ("Database Integration", 90, "Connect an API to a database and handle errors."),
        ("Mini Backend Project", 120, "Build and document a small CRUD application."),
    ],
    "System Design Basics": [
        ("Client, Server and Database", 60, "Draw a basic architecture and describe each component."),
        ("Caching, Scaling and Reliability", 90, "Learn the purpose and trade-offs of each concept."),
    ],
    "Python for Data Analysis": [
        ("Pandas DataFrames", 75, "Load a dataset and inspect columns and missing values."),
        ("Data Cleaning", 90, "Handle missing values, duplicates and incorrect types."),
        ("Exploratory Data Analysis", 90, "Summarize distributions and relationships."),
    ],
    "Statistics": [
        ("Descriptive Statistics", 60, "Practice mean, median, variance and standard deviation."),
        ("Probability and Distributions", 90, "Solve simple probability exercises."),
        ("Correlation and Sampling", 75, "Interpret relationships without assuming causation."),
    ],
    "Data Visualization": [
        ("Charts and Choosing Visuals", 60, "Create charts that answer specific questions."),
        ("Build a Dashboard", 120, "Create a compact dashboard from a sample dataset."),
    ],
    "Excel or Spreadsheets": [
        ("Formulas and Sorting", 60, "Practice common formulas and data filters."),
        ("Pivot Tables and Lookups", 75, "Summarize a small business dataset."),
    ],
    "Dashboard Projects": [
        ("Define Metrics", 45, "Choose questions and metrics before creating visuals."),
        ("Build an Analysis Dashboard", 120, "Create a small dashboard and explain the findings."),
    ],
    "Python for Data Science": [
        ("Python Data Handling", 75, "Practice lists, dictionaries, functions and files."),
        ("NumPy and Pandas", 90, "Load and transform a small dataset."),
    ],
    "Statistics and Linear Algebra": [
        ("Vectors and Matrices", 75, "Practice vector operations and matrix multiplication."),
        ("Probability and Statistics Review", 90, "Review distributions and summary measures."),
    ],
    "Data Cleaning and Feature Engineering": [
        ("Missing Values and Outliers", 75, "Inspect and document data quality issues."),
        ("Encoding and Scaling", 90, "Compare common preprocessing approaches."),
    ],
    "Machine Learning Algorithms": [
        ("Train a Baseline Model", 90, "Train a simple model with a train/test split."),
        ("Compare Two Algorithms", 120, "Compare models using a suitable metric."),
    ],
    "Model Evaluation": [
        ("Train/Test Split and Metrics", 75, "Choose metrics that match the problem."),
        ("Cross Validation and Error Analysis", 90, "Inspect errors and check for leakage."),
    ],
    "APIs and Model Deployment": [
        ("Save and Load a Model", 60, "Persist a trained model and load it again."),
        ("Serve Predictions with an API", 120, "Create and test a prediction endpoint."),
    ],
}

def normalize(value):
    return value.strip().lower().replace("-", " ")

def analyze_gaps(target_role, known_skills, level):
    requirements = CAREER_REQUIREMENTS.get(target_role, [])
    known = {normalize(skill) for skill in known_skills}
    aliases = {
        "dsa": "data structures and algorithms",
        "oop": "object oriented programming",
        "object oriented programming": "object oriented programming",
        "python": "python for data science",
        "data analysis": "python for data analysis",
        "machine learning": "machine learning algorithms",
        "database": "sql and databases",
        "sql": "sql and databases",
        "git": "git and github",
        "github": "git and github",
        "api": "rest apis",
        "fastapi": "rest apis",
    }
    known_expanded = set(known)
    for skill in known:
        if skill in aliases:
            known_expanded.add(aliases[skill])
    gaps = []
    for skill, priority, reason in requirements:
        if normalize(skill) not in known_expanded:
            gaps.append({
                "skill": skill,
                "priority": priority,
                "reason": reason,
                "current_level": "Not listed",
                "required_level": "Working knowledge",
            })
        elif level == "Beginner" and priority == "High":
            gaps.append({
                "skill": skill,
                "priority": "Medium",
                "reason": f"You listed this skill; consider validating your proficiency. {reason}",
                "current_level": "Self-reported beginner",
                "required_level": "Working knowledge",
            })
    return gaps

def build_roadmap(target_role, gaps):
    roadmap = []
    for gap in gaps:
        skill = gap["skill"]
        topics = TOPIC_PLANS.get(skill, [(f"{skill}: fundamentals", 60, f"Learn the core concepts of {skill} and complete a small exercise.")])
        roadmap.append({
            "skill": skill,
            "priority": gap["priority"],
            "topics": topics,
        })
    return roadmap

def make_tasks(roadmap, hours_per_day, start_date):
    daily_capacity = max(30, int(hours_per_day * 60))
    tasks = []
    day_number = 1
    minutes_used = 0
    for section in roadmap:
        for title, minutes, description in section["topics"]:
            # Keep a task intact; if it does not fit, begin a new day.
            if minutes_used and minutes_used + minutes > daily_capacity:
                day_number += 1
                minutes_used = 0
            due = start_date + timedelta(days=day_number - 1)
            tasks.append({
                "day_number": day_number,
                "title": title,
                "description": f"{section['skill']}: {description}",
                "estimated_minutes": minutes,
                "due_date": due.isoformat(),
                "skill": section["skill"],
                "resources": resources_for_task(section["skill"], title),
            })
            minutes_used += minutes
            if minutes_used >= daily_capacity:
                day_number += 1
                minutes_used = 0
    return tasks

def reschedule_incomplete(student_id, today):
    from database import connect, get_tasks
    tasks = get_tasks(student_id)
    remaining = [t for t in tasks if t["status"] != "Completed"]
    next_day = 1
    with connect() as conn:
        for task in remaining:
            new_due = today + timedelta(days=next_day - 1)
            conn.execute(
                "UPDATE tasks SET day_number = ?, due_date = ? WHERE id = ?",
                (next_day, new_due.isoformat(), task["id"])
            )
            next_day += 1
