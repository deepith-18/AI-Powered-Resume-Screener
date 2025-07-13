

#AI-Powered Resume Screener#

![alt text](https://img.shields.io/badge/Python-3.9%2B-blue.svg)


![alt text](https://img.shields.io/badge/Django-4.2-blue.svg)


![alt text](https://img.shields.io/badge/License-MIT-yellow.svg)

An intelligent, modern web application designed to automate and streamline the initial stages of recruitment. This tool uses state-of-the-art AI models to rank candidate resumes against a job description, identify skill gaps, and filter out irrelevant documents, saving recruiters countless hours of manual work.

(Note: You should replace the link above with a real screenshot of your application's dashboard!)

✨ Features

Semantic Ranking: Goes beyond simple keyword matching. It uses Sentence-BERT models to understand the contextual meaning of the job description and resumes, providing a far more accurate "match score".

Skill Gap Analysis: Automatically extracts required skills from the job description and compares them against the skills found in each resume, instantly highlighting any missing qualifications.

Intelligent Document Classification: Uses a zero-shot classification model to determine if an uploaded file is actually a resume, automatically skipping irrelevant documents like cover letters, certificates, or invoices.

Asynchronous Processing: Leverages Celery and Redis to handle the computationally-intensive AI processing in the background. This means you can upload hundreds of resumes and the UI remains fast and responsive.

Interactive Dashboard: A clean, modern interface to view ranked results. Features include:

Filtering candidates by minimum match score.

Filtering candidates by a specific skill.

A "shortlist" feature to flag promising candidates.

Export to Excel: Easily export the details of your shortlisted candidates into a well-formatted .xlsx file for sharing or further analysis.

Modern UI/UX: A sleek, dark-themed interface with an animated background powered by Vanta.js for a professional feel.

🛠️ Tech Stack

Backend: Django, Celery

AI / Machine Learning:

transformers (Hugging Face) for Zero-Shot Classification

sentence-transformers for Semantic Similarity & Embeddings

PyTorch as the ML framework

Database: SQLite3 (default, easily switchable)

Task Queue / Broker: Redis

File Processing: PyMuPDF (for robust PDF text extraction), Pandas (for Excel export)

Frontend: HTML, CSS, JavaScript, Vanta.js (for animated background)

🚀 Getting Started

Follow these instructions to get the project up and running on your local machine.

1. Prerequisites

Make sure you have the following installed:

Python 3.9 or higher

Git for cloning the repository

Redis: The message broker for Celery.

Download and Installation Guide for Redis

2. Installation and Setup

Step 1: Clone the Repository

Generated bash
git clone https://github.com/your-username/screener-project.git
cd screener-project


Step 2: Create and Activate a Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.

On Windows:

Generated bash
python -m venv venv
.\venv\Scripts\activate
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

On macOS/Linux:

Generated bash
python3 -m venv venv
source venv/bin/activate
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Step 3: Install Required Packages
Create a requirements.txt file in your project's root directory with the following content:

Generated txt
# requirements.txt
django
celery
redis
PyMuPDF
pandas
openpyxl
transformers
sentence-transformers
torch
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Txt
IGNORE_WHEN_COPYING_END

Now, install all packages using pip:

Generated bash
pip install -r requirements.txt
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Note: The first time you run the app, the AI models (all-MiniLM-L6-v2 and bart-large-mnli) will be downloaded automatically. This may take a few minutes and requires an internet connection.

Step 4: Apply Database Migrations
This will set up the necessary tables in your database.

Generated bash
python manage.py migrate
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END
3. Running the Application

This application requires three separate terminal windows to run correctly: one for the Redis server, one for the Celery worker, and one for the Django development server.

Terminal 1: Start the Redis Server
Navigate to your Redis installation directory or ensure redis-server is in your PATH, then run:

Generated bash
redis-server
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

You should see the Redis logo and log messages indicating it is ready to accept connections.

Terminal 2: Start the Celery Worker
In your project directory (with the virtual environment activated), start the Celery worker. This process will wait for and execute background tasks (like processing resumes).

Generated bash
celery -A screener_project worker -l info
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Terminal 3: Start the Django Development Server
Finally, run the main web application.

Generated bash
python manage.py runserver
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

You can now access the application by navigating to http://127.0.0.1:8000/ in your web browser.

📖 How to Use

Open the Application: Go to http://127.0.0.1:8000/.

Paste Job Description: Copy the full text of the job description you are hiring for into the first text area.

Upload Resumes: Click the "Choose Files" button and select one or more PDF resume files.

Rank Resumes: Click the "Rank Resumes" button. You will be redirected to the dashboard immediately. The results will appear as the Celery workers process the files in the background. You may need to refresh the page after a few moments.

Analyze Results:

The dashboard shows each resume, its match score, and a skill gap analysis.

Use the filter controls at the top to narrow down the results by score or required skills.

Click the star icon to "shortlist" a candidate.

Export: Click the "Export Shortlisted to Excel" button to download a spreadsheet of your selected candidates.

📁 Project Structure
Generated code
screener_project/
├── media/                  # Uploaded resume files are stored here
├── resumes/                # The main Django app
│   ├── migrations/
│   ├── templates/
│   │   └── resumes/
│   │       ├── dashboard.html  # The main UI template (consolidated)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py           # Defines the Resume and ScreeningResult database models
│   ├── tasks.py            # Defines the Celery background task for processing resumes
│   ├── tests.py
│   ├── urls.py             # App-level URL routing
│   ├── utils.py            # Helper functions (PDF extraction, skill extraction)
│   └── views.py            # Core application logic (request handling, filtering, etc.)
├── screener_project/       # The Django project configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py         # Project settings (INSTALLED_APPS, DB, Celery config)
│   ├── urls.py             # Project-level URL routing
│   └── wsgi.py
├── manage.py               # Django's command-line utility
└── requirements.txt        # List of Python dependencies
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END
💡 Future Improvements

User Authentication: Implement user accounts so multiple recruiters can manage their own screening sessions.

Job Position Management: Allow users to save job descriptions and associate screenings with them.

Enhanced Skill Database: Move the SKILLS_DB to a database table to make it easily editable through an admin interface.

Real-time Updates: Use Django Channels or frontend polling to update the dashboard in real-time as results are processed, without needing a page refresh.

Dockerize the Application: Create Dockerfile and docker-compose.yml files to make setup even easier and more consistent across different environments.

📄 License

This project is licensed under the MIT License. See the LICENSE file for details.
