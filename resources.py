"""Curated learning resources for roadmap tasks.

Website links are curated resources. Video suggestions use a topic-specific YouTube
search URL instead of hard-coding a potentially outdated or misleading video ID.
"""
from urllib.parse import quote_plus

RESOURCE_CATALOG = {
    "Data Structures and Algorithms": [
        {"title": "VisuAlgo — visualise algorithms", "url": "https://visualgo.net/en", "kind": "Interactive practice"},
        {"title": "GeeksforGeeks — DSA tutorials", "url": "https://www.geeksforgeeks.org/data-structures/", "kind": "Tutorial"},
        {"title": "LeetCode — coding practice", "url": "https://leetcode.com/problemset/", "kind": "Practice"},
    ],
    "Object-Oriented Programming": [
        {"title": "Python classes documentation", "url": "https://docs.python.org/3/tutorial/classes.html", "kind": "Documentation"},
        {"title": "Programiz — OOP concepts", "url": "https://www.programiz.com/python-programming/object-oriented-programming", "kind": "Tutorial"},
    ],
    "SQL and Databases": [
        {"title": "SQLBolt — interactive SQL lessons", "url": "https://sqlbolt.com/", "kind": "Interactive tutorial"},
        {"title": "PostgreSQL tutorial", "url": "https://www.postgresql.org/docs/current/tutorial.html", "kind": "Documentation"},
    ],
    "Git and GitHub": [
        {"title": "Pro Git book", "url": "https://git-scm.com/book/en/v2", "kind": "Free book"},
        {"title": "GitHub Skills — hands-on courses", "url": "https://skills.github.com/", "kind": "Interactive practice"},
    ],
    "REST APIs": [
        {"title": "MDN — HTTP overview", "url": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview", "kind": "Documentation"},
        {"title": "FastAPI tutorial", "url": "https://fastapi.tiangolo.com/tutorial/", "kind": "Hands-on tutorial"},
    ],
    "Backend Development": [
        {"title": "FastAPI tutorial", "url": "https://fastapi.tiangolo.com/tutorial/", "kind": "Hands-on tutorial"},
        {"title": "Python official tutorial", "url": "https://docs.python.org/3/tutorial/", "kind": "Documentation"},
    ],
    "System Design Basics": [
        {"title": "System Design Primer", "url": "https://github.com/donnemartin/system-design-primer", "kind": "Open-source guide"},
        {"title": "roadmap.sh — software design", "url": "https://roadmap.sh/software-design-architecture", "kind": "Learning roadmap"},
    ],
    "Python for Data Analysis": [
        {"title": "pandas getting started", "url": "https://pandas.pydata.org/docs/getting_started/intro_tutorials/", "kind": "Documentation"},
        {"title": "Kaggle Learn — Pandas", "url": "https://www.kaggle.com/learn/pandas", "kind": "Interactive course"},
    ],
    "Statistics": [
        {"title": "Khan Academy — statistics and probability", "url": "https://www.khanacademy.org/math/statistics-probability", "kind": "Free lessons"},
        {"title": "OpenStax — Introductory Statistics", "url": "https://openstax.org/details/books/introductory-statistics", "kind": "Free textbook"},
    ],
    "Data Visualization": [
        {"title": "Matplotlib tutorials", "url": "https://matplotlib.org/stable/tutorials/", "kind": "Documentation"},
        {"title": "Kaggle Learn — Data Visualization", "url": "https://www.kaggle.com/learn/data-visualization", "kind": "Interactive course"},
    ],
    "Excel or Spreadsheets": [
        {"title": "Microsoft Excel help and learning", "url": "https://support.microsoft.com/excel", "kind": "Official tutorials"},
        {"title": "GCFGlobal — Excel", "url": "https://edu.gcfglobal.org/en/excel/", "kind": "Free lessons"},
    ],
    "Dashboard Projects": [
        {"title": "Tableau free training videos", "url": "https://www.tableau.com/learn/training", "kind": "Training"},
        {"title": "Power BI learning", "url": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi/", "kind": "Official learning path"},
    ],
    "Python for Data Science": [
        {"title": "Python official tutorial", "url": "https://docs.python.org/3/tutorial/", "kind": "Documentation"},
        {"title": "Kaggle Learn — Python", "url": "https://www.kaggle.com/learn/python", "kind": "Interactive course"},
        {"title": "NumPy quickstart", "url": "https://numpy.org/doc/stable/user/quickstart.html", "kind": "Documentation"},
    ],
    "Statistics and Linear Algebra": [
        {"title": "Khan Academy — linear algebra", "url": "https://www.khanacademy.org/math/linear-algebra", "kind": "Free lessons"},
        {"title": "Khan Academy — statistics and probability", "url": "https://www.khanacademy.org/math/statistics-probability", "kind": "Free lessons"},
    ],
    "Data Cleaning and Feature Engineering": [
        {"title": "scikit-learn — preprocessing data", "url": "https://scikit-learn.org/stable/modules/preprocessing.html", "kind": "Documentation"},
        {"title": "Kaggle Learn — Data Cleaning", "url": "https://www.kaggle.com/learn/data-cleaning", "kind": "Interactive course"},
    ],
    "Machine Learning Algorithms": [
        {"title": "Google — Machine Learning Crash Course", "url": "https://developers.google.com/machine-learning/crash-course", "kind": "Free course"},
        {"title": "scikit-learn user guide", "url": "https://scikit-learn.org/stable/user_guide.html", "kind": "Documentation"},
    ],
    "Model Evaluation": [
        {"title": "scikit-learn — model evaluation", "url": "https://scikit-learn.org/stable/modules/model_evaluation.html", "kind": "Documentation"},
        {"title": "Google — Machine Learning Crash Course", "url": "https://developers.google.com/machine-learning/crash-course", "kind": "Free course"},
    ],
    "APIs and Model Deployment": [
        {"title": "FastAPI tutorial", "url": "https://fastapi.tiangolo.com/tutorial/", "kind": "Hands-on tutorial"},
        {"title": "scikit-learn — model persistence", "url": "https://scikit-learn.org/stable/model_persistence.html", "kind": "Documentation"},
    ],
}

DEFAULT_RESOURCES = [
    {"title": "roadmap.sh — developer learning roadmaps", "url": "https://roadmap.sh/", "kind": "Learning roadmap"},
    {"title": "MIT OpenCourseWare", "url": "https://ocw.mit.edu/", "kind": "Free course materials"},
]


def resources_for_task(skill: str, topic: str) -> list[dict[str, str]]:
    """Return curated website links plus a topic-specific video search suggestion."""
    resources = [dict(item) for item in RESOURCE_CATALOG.get(skill, DEFAULT_RESOURCES)]
    query = quote_plus(f"{skill} {topic} tutorial for beginners")
    resources.append({
        "title": f"Video suggestions: {skill} — {topic}",
        "url": f"https://www.youtube.com/results?search_query={query}",
        "kind": "YouTube video search",
    })
    return resources
