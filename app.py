from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "portfolio-dev-secret")

BASE_DIR = Path(__file__).resolve().parent
MESSAGES_FILE = BASE_DIR / "data" / "messages.json"

PROFILE = {
    "name": "Manish Saini",
    "role": "AI Intern | Aspiring Data Scientist | GenAI Builder",
    "tagline": "I build AI, NLP, RAG, and Flask-based products that turn practical ideas into working systems.",
    "location": "Jaipur, Rajasthan, India",
    "email": "manishchanwara0832@gmail.com",
    "phone": "+91 9057054834",
    "github": "https://github.com/manish0832",
    "github_username": "manish0832",
    "linkedin": "https://www.linkedin.com/in/manish-saini-8627a0314",
    "resume_file": "resume/Manish_Saini_Resume.pdf",
    "career_goal": "To become a Data Scientist while growing into AI Engineering, Generative AI, NLP, and Machine Learning roles.",
    "current_role": "AI Intern at Business Now Pvt Ltd, Jaipur",
    "education": "B.Tech in Computer Science, Bhartiya Institute of Engineering and Technology",
    "training": "Data Science Training in AI, ML, and Python at Grras Solutions Pvt. Ltd.",
    "hero_stats": [
        {"label": "Current Role", "value": "AI Intern"},
        {"label": "Specialization", "value": "GenAI, NLP, RAG"},
        {"label": "Projects", "value": "12+ End-to-End"},
    ],
}

SKILL_GROUPS = {
    "Programming": ["Python", "JavaScript", "SQL"],
    "Web Development": ["HTML", "CSS", "Flask", "API Integration", "Database Integration"],
    "Data Science & ML": [
        "Statistics",
        "NumPy",
        "Pandas",
        "Seaborn",
        "Scikit-learn",
        "Machine Learning",
        "Artificial Intelligence",
    ],
    "AI & GenAI": [
        "Retrieval-Augmented Generation (RAG)",
        "Semantic Search",
        "Embeddings",
        "NLP",
        "AI Agents",
        "MCP (Model Context Protocol)",
    ],
    "Other": ["Web Scraping"],
}

SKILLS = [item for values in SKILL_GROUPS.values() for item in values]

EXPERIENCE = [
    {
        "title": "AI Intern",
        "company": "Business Now Pvt Ltd",
        "location": "Jaipur",
        "period": "Current",
        "summary": "Working on applied AI solutions with exposure to modern tooling, product thinking, and real-world delivery expectations.",
    },
    {
        "title": "AI/ML Intern",
        "company": "Pedestal Techno World Pvt. Ltd.",
        "location": "Jaipur",
        "period": "Previous Internship",
        "summary": "Built and supported machine learning workflows, preprocessing tasks, and practical AI project implementations.",
    },
    {
        "title": "Data Science Trainee",
        "company": "Grras Solutions Pvt. Ltd.",
        "location": "Jaipur",
        "period": "Training",
        "summary": "Focused on AI, ML, Python, data analysis, and model-building fundamentals with hands-on project work.",
    },
]

PROJECTS = [
    {
        "title": "RAG Pipeline / Knowledge Assistant",
        "description": "Built a retrieval-augmented workflow for question answering over custom knowledge sources using embeddings and semantic retrieval.",
        "category": "Generative AI",
        "stack": ["Python", "RAG", "Embeddings", "Semantic Search"],
        "impact": "Demonstrates practical GenAI architecture beyond simple prompting.",
        "accent": "sunset",
    },
    {
        "title": "AI Resume Analyzer (ATS Scoring System)",
        "description": "Analyzes resumes, evaluates ATS-style fit, and provides optimization suggestions using NLP-oriented logic.",
        "category": "NLP",
        "stack": ["Python", "Flask", "NLP"],
        "impact": "Transforms resume review into a faster and more actionable workflow.",
        "accent": "ocean",
    },
    {
        "title": "AI Resume Builder",
        "description": "Structured assistant for generating stronger resume content with better formatting and role-focused positioning.",
        "category": "Generative AI",
        "stack": ["Python", "Prompting", "Flask"],
        "impact": "Helps users create clearer and more targeted resumes.",
        "accent": "plum",
    },
    {
        "title": "Mental Health Early Warning System",
        "description": "Explores predictive indicators and early detection ideas using data-driven signals and ML support.",
        "category": "Machine Learning",
        "stack": ["Python", "ML", "Data Analysis"],
        "impact": "Applies AI to a meaningful social problem space.",
        "accent": "forest",
    },
    {
        "title": "Job Analysis Project",
        "description": "Analyzed jobs, skills, and requirements to identify patterns and decision-making insights for candidates.",
        "category": "Data Science",
        "stack": ["Python", "Pandas", "Visualization"],
        "impact": "Supports data-backed understanding of hiring trends and skill gaps.",
        "accent": "gold",
    },
    {
        "title": "Jarvis Voice Assistant",
        "description": "Voice assistant experiment for command execution, automation, and natural interaction flows.",
        "category": "AI Assistant",
        "stack": ["Python", "Speech", "Automation"],
        "impact": "Showcases conversational interaction and local task automation.",
        "accent": "ember",
    },
    {
        "title": "Flask-Based Voice Assistant",
        "description": "Wrapped assistant behaviors into a Flask-driven interface for a more accessible and testable workflow.",
        "category": "AI Assistant",
        "stack": ["Flask", "Python", "Voice UI"],
        "impact": "Brings assistant logic into a web-first experience.",
        "accent": "sunset",
    },
    {
        "title": "Voice-Controlled Task Manager (Jarvis++)",
        "description": "Extended assistant concept that supports productivity and task routing through voice interaction.",
        "category": "AI Assistant",
        "stack": ["Python", "Automation", "Voice Commands"],
        "impact": "Explores hands-free personal productivity systems.",
        "accent": "ocean",
    },
    {
        "title": "Career Path Visualizer",
        "description": "Maps user skills to possible career directions and learning pathways using structured logic and analysis.",
        "category": "Data Science",
        "stack": ["Python", "Analytics", "Visualization"],
        "impact": "Turns skill assessment into a clearer decision-making tool.",
        "accent": "plum",
    },
    {
        "title": "Cricket Match Performance Evaluation System",
        "description": "Performance-focused analytics project for understanding match and player metrics more effectively.",
        "category": "Data Science",
        "stack": ["Python", "Statistics", "Pandas"],
        "impact": "Applies analytics to sports performance evaluation.",
        "accent": "forest",
    },
    {
        "title": "Housing Data Analysis / Prediction",
        "description": "Analyzed housing datasets and explored prediction workflows using ML and feature-driven reasoning.",
        "category": "Machine Learning",
        "stack": ["Python", "Scikit-learn", "Data Visualization"],
        "impact": "Demonstrates practical predictive modeling skills.",
        "accent": "gold",
    },
    {
        "title": "Shoe Shopping Web Application",
        "description": "Responsive e-commerce web application with product flows, structured UI, and backend integration thinking.",
        "category": "Web Development",
        "stack": ["Flask", "SQL", "HTML/CSS"],
        "impact": "Shows full-stack product-building ability beyond AI use cases.",
        "accent": "ember",
    },
    {
        "title": "Portfolio Website (Flask)",
        "description": "Personal portfolio rebuilt with Flask, modern UI styling, dynamic data, and polished frontend interactions.",
        "category": "Web Development",
        "stack": ["Flask", "JavaScript", "Responsive UI"],
        "impact": "Presents technical profile in a more professional and current format.",
        "accent": "sunset",
    },
    {
        "title": "Library Management System",
        "description": "Role-based library platform for book records, users, and transactional workflows.",
        "category": "Web Development",
        "stack": ["Flask", "SQL", "Database Integration"],
        "impact": "Improves organization and workflow tracking in a practical domain.",
        "accent": "ocean",
    },
    {
        "title": "Weather App",
        "description": "Lightweight weather experience using API integration and responsive UI behavior.",
        "category": "Web Development",
        "stack": ["APIs", "Flask", "JavaScript"],
        "impact": "Demonstrates real-time external data integration.",
        "accent": "plum",
    },
]

SERVICES = [
    "AI and GenAI prototypes",
    "RAG and knowledge assistant workflows",
    "Flask web application development",
    "Data analysis and machine learning projects",
]

HIGHLIGHTS = [
    "Real AI internship experience",
    "RAG pipeline experience",
    "Flask development experience",
    "Multiple end-to-end AI projects",
    "Exposure to MCP concepts and AI agents",
    "Data science and machine learning background",
]


def save_message(payload: dict) -> None:
    MESSAGES_FILE.parent.mkdir(parents=True, exist_ok=True)
    messages = []
    if MESSAGES_FILE.exists():
        try:
            messages = json.loads(MESSAGES_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            messages = []

    messages.append(payload)
    MESSAGES_FILE.write_text(json.dumps(messages, indent=2), encoding="utf-8")


def build_context() -> dict:
    return {
        "profile": PROFILE,
        "skills": SKILLS,
        "skill_groups": SKILL_GROUPS,
        "experience": EXPERIENCE,
        "projects": PROJECTS,
        "services": SERVICES,
        "highlights": HIGHLIGHTS,
        "year": datetime.now().year,
    }


@app.route("/")
def home():
    return render_template("index.html", **build_context())


@app.route("/about")
def about():
    return render_template("about.html", **build_context())


@app.route("/projects")
def projects_page():
    return render_template("projects.html", **build_context())


@app.route("/resume")
def resume():
    return render_template("resume.html", **build_context())


@app.route("/contact", methods=["GET", "POST"])
def contact():
    context = build_context()
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()

        if not all([name, email, subject, message]):
            flash("Please complete every field before sending your message.", "error")
            return render_template("contact.html", **context), 400

        payload = {
            "name": name,
            "email": email,
            "subject": subject,
            "message": message,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        save_message(payload)
        flash("Thanks for reaching out. Your message has been saved successfully.", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html", **context)


@app.route("/api/projects")
def projects_api():
    category = request.args.get("category", "").strip().lower()
    query = request.args.get("q", "").strip().lower()

    filtered = PROJECTS
    if category:
        filtered = [project for project in filtered if project["category"].lower() == category]
    if query:
        filtered = [
            project
            for project in filtered
            if query in project["title"].lower() or query in project["description"].lower()
        ]

    return jsonify(
        {
            "count": len(filtered),
            "projects": filtered,
            "availableCategories": sorted({project["category"] for project in PROJECTS}),
        }
    )


@app.route("/api/profile")
def profile_api():
    return jsonify(
        {
            "profile": PROFILE,
            "skills": SKILLS,
            "skillGroups": SKILL_GROUPS,
            "experience": EXPERIENCE,
            "services": SERVICES,
            "highlights": HIGHLIGHTS,
        }
    )


@app.route("/health")
def healthcheck():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
