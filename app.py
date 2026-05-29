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
    "role": "AI Engineer | Data Scientist | RAG Developer",
    "tagline": "AI Intern building recruiter-ready products across RAG, NLP, machine learning, and data science.",
    "location": "Jaipur, Rajasthan, India",
    "email": "manishchanwara0832@gmail.com",
    "phone": "+91 9057054834",
    "github": "https://github.com/manish0832",
    "github_username": "manish0832",
    "linkedin": "https://www.linkedin.com/in/manish-saini-8627a0314",
    "resume_file": "resume/Manish_Saini_Resume.pdf",
    "career_goal": "To grow into AI Engineer, Generative AI Engineer, NLP Engineer, and Data Scientist roles by delivering strong end-to-end products.",
    "current_role": "AI Intern at Business Now Pvt Ltd, Jaipur",
    "education": "B.Tech in Computer Science, Bhartiya Institute of Engineering and Technology",
    "training": "Data Science training in AI, ML, and Python at Grras Solutions Pvt. Ltd.",
    "hero_rotations": [
        "Building AI Solutions...",
        "Shipping Recruiter-Ready Projects...",
        "Developing RAG Systems...",
        "Designing Data Science Workflows...",
    ],
    "hero_stats": [
        {"label": "Projects", "value": "15+", "tone": "primary"},
        {"label": "AI Models", "value": "8+", "tone": "cyan"},
        {"label": "Internships", "value": "2", "tone": "gold"},
        {"label": "Skills", "value": "20+", "tone": "violet"},
    ],
}

SKILL_GROUPS = {
    "Programming": [
        {"name": "Python", "level": 98},
        {"name": "SQL", "level": 88},
        {"name": "JavaScript", "level": 76},
    ],
    "AI / ML": [
        {"name": "Machine Learning", "level": 95},
        {"name": "NLP", "level": 91},
        {"name": "RAG", "level": 90},
        {"name": "Scikit-learn", "level": 86},
    ],
    "Data Science": [
        {"name": "Pandas", "level": 92},
        {"name": "NumPy", "level": 88},
        {"name": "Statistics", "level": 84},
        {"name": "Data Visualization", "level": 82},
    ],
    "Backend": [
        {"name": "Flask", "level": 90},
        {"name": "APIs", "level": 84},
        {"name": "MySQL", "level": 80},
        {"name": "REST Workflows", "level": 82},
    ],
}

SKILLS = [item["name"] for values in SKILL_GROUPS.values() for item in values]

TIMELINE = [
    {"year": "2022", "title": "Started B.Tech", "detail": "Began Computer Science journey with a strong focus on software foundations."},
    {"year": "2024", "title": "AI/ML Internship", "detail": "Worked as AI/ML Intern at Pedestal Techno World Pvt. Ltd."},
    {"year": "2025", "title": "Data Science Training", "detail": "Advanced training in AI, ML, Python, and data science workflows at Grras Solutions."},
    {"year": "2026", "title": "AI Intern", "detail": "Currently working at Business Now Pvt Ltd, Jaipur on applied AI solutions."},
]

EXPERIENCE = [
    {
        "year": "2026",
        "title": "AI Intern",
        "company": "Business Now Pvt Ltd",
        "location": "Jaipur",
        "period": "Current Role",
        "summary": "Working on applied AI solutions with product thinking, iteration speed, and real-world delivery expectations.",
        "achievements": [
            "Contributed to production-oriented AI workflows",
            "Worked with modern AI implementation patterns",
        ],
    },
    {
        "year": "2025",
        "title": "Data Science Trainee",
        "company": "Grras Solutions Pvt. Ltd.",
        "location": "Jaipur",
        "period": "Training",
        "summary": "Focused on Python, ML, analytics, and model-building through practical project work.",
        "achievements": [
            "Strengthened ML and data analysis fundamentals",
            "Built multiple end-to-end training projects",
        ],
    },
    {
        "year": "2024",
        "title": "AI/ML Intern",
        "company": "Pedestal Techno World Pvt. Ltd.",
        "location": "Jaipur",
        "period": "Previous Internship",
        "summary": "Built and supported ML workflows, preprocessing tasks, and practical AI implementations.",
        "achievements": [
            "Handled data preprocessing and model experimentation",
            "Gained hands-on exposure to applied AI work",
        ],
    },
]

FEATURED_PROJECTS = [
    {
        "mission": "Mission 001",
        "title": "AI Resume Analyzer",
        "description": "ATS scoring system that evaluates resumes and returns optimization suggestions with NLP-oriented logic.",
        "category": "AI",
        "stack": ["Python", "Flask", "NLP", "Machine Learning"],
        "impact": "ATS Score Prediction",
        "status": "Completed",
        "accent": "ocean",
    },
    {
        "mission": "Mission 002",
        "title": "Mental Health Early Warning System",
        "description": "Predictive system exploring early warning signals with sentiment and behavioral pattern analysis.",
        "category": "ML",
        "stack": ["Python", "ML", "Analytics"],
        "impact": "Early Detection Modeling",
        "status": "Completed",
        "accent": "forest",
    },
    {
        "mission": "Mission 003",
        "title": "Jarvis AI Assistant",
        "description": "Voice-driven assistant for command execution, workflow automation, and smart interactions.",
        "category": "AI",
        "stack": ["Python", "Voice", "Automation"],
        "impact": "AI Productivity Assistant",
        "status": "Completed",
        "accent": "plum",
    },
    {
        "mission": "Mission 004",
        "title": "Career Path Visualizer",
        "description": "Recommendation engine for skills, future roles, and structured learning directions.",
        "category": "Data Science",
        "stack": ["Python", "Analytics", "Visualization"],
        "impact": "Skill Recommendation Engine",
        "status": "Completed",
        "accent": "gold",
    },
    {
        "mission": "Mission 005",
        "title": "RAG Document Assistant",
        "description": "Document Q&A workflow that uses embeddings, retrieval, and context-aware answering over knowledge bases.",
        "category": "AI",
        "stack": ["Python", "RAG", "Embeddings", "Semantic Search"],
        "impact": "Retrieval-Augmented Question Answering",
        "status": "Completed",
        "accent": "sunset",
    },
    {
        "mission": "Mission 006",
        "title": "Shoe Shopping Web App",
        "description": "Responsive e-commerce product experience with structured browsing and backend integration thinking.",
        "category": "Flask",
        "stack": ["Flask", "SQL", "HTML/CSS"],
        "impact": "E-commerce Workflow UI",
        "status": "Completed",
        "accent": "ember",
    },
]

ALL_PROJECTS = FEATURED_PROJECTS + [
    {
        "mission": "Mission 007",
        "title": "AI Resume Builder",
        "description": "Structured assistant for generating stronger resume content with better formatting and positioning.",
        "category": "AI",
        "stack": ["Python", "Flask", "Prompting"],
        "impact": "Resume Generation Workflow",
        "status": "Completed",
        "accent": "sunset",
    },
    {
        "mission": "Mission 008",
        "title": "Flask-Based Voice Assistant",
        "description": "Web-first assistant experience built around Flask and voice-oriented controls.",
        "category": "Flask",
        "stack": ["Flask", "Python", "Voice UI"],
        "impact": "Browser-Accessible Assistant",
        "status": "Completed",
        "accent": "ocean",
    },
    {
        "mission": "Mission 009",
        "title": "Housing Data Analysis / Prediction",
        "description": "Predictive modeling workflow over housing datasets using exploratory analysis and ML techniques.",
        "category": "ML",
        "stack": ["Python", "Scikit-learn", "Visualization"],
        "impact": "Predictive Modeling Workflow",
        "status": "Completed",
        "accent": "gold",
    },
]

RAG_SHOWCASE = {
    "documents": "5000+",
    "embedding_model": "text-embedding-3-small",
    "vector_database": "Qdrant",
    "accuracy": "92%",
    "sample_questions": [
        "Summarize the indexed documents",
        "What is the best project for recruiters?",
        "Show how retrieval improves responses",
    ],
}

CERTIFICATIONS = [
    {"title": "Data Science", "issuer": "Grras Solutions", "status": "Completed"},
    {"title": "Machine Learning", "issuer": "Training Program", "status": "Completed"},
    {"title": "Python for AI", "issuer": "Training Program", "status": "Completed"},
    {"title": "Statistics for Data Science", "issuer": "Training Program", "status": "Completed"},
]

GITHUB_METRICS = {
    "repositories": "30+",
    "commits": "1200+",
    "projects": "15+",
    "languages": ["Python", "SQL", "JavaScript"],
    "contributions": [8, 6, 9, 10, 7, 11, 5, 9, 12, 8, 10, 7, 6, 11],
}

ACHIEVEMENTS = [
    {"label": "Projects Completed", "value": "15+"},
    {"label": "Internships", "value": "2"},
    {"label": "Certifications", "value": "8"},
    {"label": "Technologies", "value": "20+"},
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

SIDEBAR_ITEMS = [
    "Dashboard",
    "About",
    "Skills",
    "Projects",
    "Experience",
    "Certifications",
    "Analytics",
    "Mandee AI",
    "Contact",
]

ASSISTANT_SUGGESTIONS = [
    "Tell me about Manish.",
    "Explain the RAG project.",
    "Show experience.",
    "Download resume.",
    "What technologies does he know?",
]

ASSISTANT_FEATURES = [
    "Experience overview",
    "Project breakdowns",
    "RAG system explanation",
    "Resume guidance",
    "Skills summary",
    "Certification highlights",
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
        "timeline": TIMELINE,
        "experience": EXPERIENCE,
        "projects": ALL_PROJECTS,
        "featured_projects": FEATURED_PROJECTS,
        "services": SERVICES,
        "highlights": HIGHLIGHTS,
        "certifications": CERTIFICATIONS,
        "github_metrics": GITHUB_METRICS,
        "achievements": ACHIEVEMENTS,
        "assistant_suggestions": ASSISTANT_SUGGESTIONS,
        "assistant_features": ASSISTANT_FEATURES,
        "sidebar_items": SIDEBAR_ITEMS,
        "rag_showcase": RAG_SHOWCASE,
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

    filtered = ALL_PROJECTS
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
            "availableCategories": sorted({project["category"] for project in ALL_PROJECTS}),
        }
    )


@app.route("/api/profile")
def profile_api():
    return jsonify(
        {
            "profile": PROFILE,
            "skills": SKILLS,
            "skillGroups": SKILL_GROUPS,
            "timeline": TIMELINE,
            "experience": EXPERIENCE,
            "services": SERVICES,
            "highlights": HIGHLIGHTS,
            "certifications": CERTIFICATIONS,
            "githubMetrics": GITHUB_METRICS,
            "achievements": ACHIEVEMENTS,
            "ragShowcase": RAG_SHOWCASE,
        }
    )


@app.route("/api/assistant")
def assistant_api():
    question = request.args.get("q", "").strip().lower()

    if "rag" in question:
        answer = "The RAG Document Assistant indexes 5000+ documents, uses the text-embedding-3-small embedding model, stores vectors in Qdrant, and targets roughly 92 percent search accuracy."
    elif "experience" in question or "intern" in question:
        answer = "Manish is currently an AI Intern at Business Now Pvt Ltd, previously worked as an AI/ML Intern at Pedestal Techno World, and completed data science training at Grras Solutions."
    elif "resume" in question or "download" in question:
        answer = "You can download the resume directly from the command center hero or the dedicated resume page."
    elif "technolog" in question or "skills" in question:
        answer = "Manish works across Python, SQL, JavaScript, Flask, APIs, machine learning, NLP, RAG, scikit-learn, pandas, NumPy, statistics, and data visualization."
    else:
        answer = "Mandee AI is the portfolio command assistant for Manish Saini. It can explain projects, experience, the RAG system, certifications, skills, and resume details in a recruiter-friendly way."

    return jsonify({"answer": answer})


@app.route("/health")
def healthcheck():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
