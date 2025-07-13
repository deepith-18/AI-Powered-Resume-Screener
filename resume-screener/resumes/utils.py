# A simple list of skills. In a real-world app, this could be a database table.
SKILLS_DB = [
    'python', 'java', 'c++', 'c#', 'javascript', 'typescript', 'html', 'css', 'sql', 'nosql',
    'react', 'angular', 'vue', 'django', 'flask', 'spring', 'node.js', 'express.js',
    'git', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'terraform', 'jenkins',
    'machine learning', 'deep learning', 'pytorch', 'tensorflow', 'scikit-learn', 'pandas', 'numpy',
    'data analysis', 'data visualization', 'api', 'rest', 'graphql',
    'agile', 'scrum', 'jira', 'figma', 'communication', 'teamwork', 'problem solving'
]

def extract_skills(text):
    """Extracts skills from a given text based on the SKILLS_DB."""
    found_skills = set()
    text_lower = text.lower()
    for skill in SKILLS_DB:
        if skill.lower() in text_lower:
            found_skills.add(skill)
    return list(found_skills)


# C:\Django Project\resume-screener\resumes\utils.py

import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a given PDF file path.
    """
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"Error reading PDF file {pdf_path}: {e}")
        return ""

def extract_skills(text):
    """
    A simple keyword-based skill extractor.
    This can be improved significantly with NLP libraries like spaCy.
    """
    # Convert text to lowercase for case-insensitive matching
    text = text.lower()
    
    # A sample list of skills. You should expand this list significantly.
    SKILLS_DB = [
        'python', 'django', 'flask', 'javascript', 'react', 'vue', 'angular',
        'html', 'css', 'sql', 'mysql', 'postgresql', 'mongodb', 'git',
        'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'rest api', 'graphql',
        'machine learning', 'data analysis', 'pandas', 'numpy', 'scikit-learn',
        'tensorflow', 'pytorch', 'celery', 'redis'
    ]
    
    found_skills = set()
    for skill in SKILLS_DB:
        # Use word boundaries (\b) to avoid matching substrings (e.g., 'java' in 'javascript')
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found_skills.add(skill.capitalize()) # Store in a consistent format
            
    return list(found_skills)