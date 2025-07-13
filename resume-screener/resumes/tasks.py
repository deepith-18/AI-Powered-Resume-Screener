# resumes/tasks.py
from celery import shared_task
from .models import ScreeningResult, Resume
from .utils import extract_text_from_pdf, extract_skills # Assume these exist
# ... import your AI models ...

@shared_task
def process_single_resume(resume_id, job_description):
    # Your entire processing logic for one resume goes here.
    # Get the resume instance from the database
    resume_instance = Resume.objects.get(id=resume_id)
    resume_text = extract_text_from_pdf(resume_instance.resume_file.path)
    
    # ... (all the AI classification, scoring, skill extraction) ...
    jd_embedding = ranking_model.encode(job_description, convert_to_tensor=True)
    resume_embedding = ranking_model.encode(resume_text, convert_to_tensor=True)
    # ... etc ...

    # Create the ScreeningResult at the end
    ScreeningResult.objects.create(...)
    return f"Processed {resume_instance.resume_file.name}"