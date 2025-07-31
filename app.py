from flask import Flask, render_template, url_for

app = Flask(__name__)

# Project data for dynamic rendering
projects = [
    {
        'title': 'AI Resume Analyzer',
        'description': 'NLP-based resume parser that scores resumes and gives optimization tips.',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQqbGJ-wDbbCPWgcveKUP96G_V15-kc3DIIVez1O4Omyi9yLXde98EvJz0ACYMpPSHual8&usqp=CAU'
    },
    {
        'title': 'Career Path Visualizer',
        'description': 'Suggests career paths based on user skills and job market trends.',
        'image': 'https://images.unsplash.com/photo-1519389950473-47ba0277781c'
    },
    {
        'title': 'library management system.',
        'description': 'A web-based system to manage library books, users, and transactions with admin and user access, built using Flask, SQL, and Bootstrap.',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRfqhxhcZFQZeYth-8oqzlJ3aGBkATntH0jLA&s'
    },
    {
        'title': 'Weather App',
        'description': 'Fetches real-time weather using OpenWeatherMap API with animated UI.',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTnhcCtZR3XicKQmIxcUcdu9DWRAu65p5WKlw&s'
    },
    {
        'title': 'Jarvis++ Voice Assistant',
        'description': 'Voice-controlled assistant using Flask, Whisper, and dynamic speech commands.',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSU3oJoQjuqpYq4zja22yX0fl90Aa2ZvedzKA7IaPHJQTS3sZhXqAZzIl2OT8QkODywoS4&usqp=CAU'
    },
    {
        'title': 'Shoe Shopping Website',
        'description': 'Responsive e-commerce UI with product browsing and MySQL backend.',
        'image': 'https://s.tmimgcdn.com/scr/800x500/377700/fabulous-shoes-store-bootstrap-5-html-template_377733-original.png'
    }
]


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/projects')
def projects_page():
    return render_template("projects.html", projects=projects)

@app.route('/resume')
def resume():
    return render_template("resume.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
