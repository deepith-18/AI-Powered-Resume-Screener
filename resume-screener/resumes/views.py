# resumes/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Resume, ScreeningResult
import pypdf
import pandas as pd
import io

from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from .utils import extract_skills

# --- (No changes needed in this section) ---
ranking_model = SentenceTransformer('all-MiniLM-L6-v2')
try:
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=0)
except Exception:
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def extract_text_from_pdf(file_path):
    try:
        with open(file_path, 'rb') as pdf_file:
            reader = pypdf.PdfReader(pdf_file)
            text = ""
            num_pages = min(len(reader.pages), 2)
            for i in range(num_pages):
                page_text = reader.pages[i].extract_text()
                if page_text:
                    text += page_text
        return text[:4096]
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return ""

def screen_resumes(request):
    if request.method == 'POST':
        ScreeningResult.objects.all().delete()
        Resume.objects.all().delete()
        
        job_description = request.POST.get('job_description', '')
        uploaded_files = request.FILES.getlist('resumes')
        candidate_labels = ["resume", "job application", "certificate", "invoice", "letter"]
        resume_keywords = ['experience', 'education', 'skills', 'summary', 'objective', 'employment', 'work history']

        if job_description and uploaded_files:
            jd_skills = set(extract_skills(job_description))
            jd_embedding = ranking_model.encode(job_description, convert_to_tensor=True)

            for file in uploaded_files:
                resume_instance = Resume(resume_file=file)
                resume_instance.save()
                resume_text = extract_text_from_pdf(resume_instance.resume_file.path)
                resume_text_lower = resume_text.lower()
                
                if not resume_text.strip(): continue
                classification_result = classifier(resume_text, candidate_labels, multi_label=False)
                top_label = classification_result['labels'][0]
                top_score = classification_result['scores'][0]
                is_likely_resume = False
                if top_label in ["resume", "job application"]:
                    keyword_count = sum(1 for keyword in resume_keywords if keyword in resume_text_lower)
                    if top_score > 0.5 or keyword_count >= 2:
                        is_likely_resume = True

                if is_likely_resume:
                    resume_embedding = ranking_model.encode(resume_text, convert_to_tensor=True)
                    cosine_score = util.pytorch_cos_sim(jd_embedding, resume_embedding).item()
                    
                    resume_skills = set(extract_skills(resume_text))
                    missing_skills = sorted(list(jd_skills - resume_skills))

                    ScreeningResult.objects.create(
                        filename=file.name,
                        score=round(cosine_score * 100, 2),
                        skills=list(resume_skills),
                        missing_skills=missing_skills
                    )
        
        return redirect('dashboard')

    return render(request, 'resumes/upload.html')


# --- MODIFIED DASHBOARD VIEW ---
def dashboard(request):
    # Start with a base QuerySet, ordering by score is a nice touch
    results_qs = ScreeningResult.objects.all().order_by('-score')

    skill_query = request.GET.get('skill')
    min_score_query = request.GET.get('min_score')

    # 1. Apply DATABASE filters first (these are efficient)
    if min_score_query:
        try:
            min_score = float(min_score_query)
            results_qs = results_qs.filter(score__gte=min_score)
        except (ValueError, TypeError):
            pass # Ignore invalid score input

    # 2. Fetch the results and apply PYTHON filters for unsupported lookups
    # We convert the queryset to a list to iterate over it.
    results = list(results_qs)

    if skill_query:
        # We now filter the list 'results' using a list comprehension.
        # This check happens in Python, not in the database.
        # The check is case-insensitive for better user experience.
        skill_query_lower = skill_query.lower()
        results = [
            res for res in results 
            if res.skills and any(skill.lower() == skill_query_lower for skill in res.skills)
        ]

    # The 'results' variable is now a list, not a QuerySet, but the template doesn't care.
    return render(request, 'resumes/dashboard.html', {'results': results})


# --- (No changes needed in this section) ---
def shortlist_candidate(request, result_id):
    if request.method == 'POST':
        result = get_object_or_404(ScreeningResult, id=result_id)
        result.is_shortlisted = not result.is_shortlisted
        result.save()
    # Redirect back to the dashboard, preserving the filters
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

def export_excel(request):
    shortlisted_candidates = ScreeningResult.objects.filter(is_shortlisted=True)
    
    data = {
        "Filename": [c.filename for c in shortlisted_candidates],
        "Score": [c.score for c in shortlisted_candidates],
        "Skills Found": [', '.join(c.skills) for c in shortlisted_candidates],
        "Missing Skills": [', '.join(c.missing_skills) for c in shortlisted_candidates],
    }
    df = pd.DataFrame(data)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Shortlisted')
    
    output.seek(0)
    
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="shortlisted_candidates.xlsx"'
    
    return response

# resumes/views.py -> screen_resumes()
from .tasks import process_single_resume

def screen_resumes(request):
    if request.method == 'POST':
        # ... get job_description and uploaded_files ...
        for file in uploaded_files:
            # Just save the file, don't process it here
            resume_instance = Resume(resume_file=file)
            resume_instance.save()
            # Call the background task!
            process_single_resume.delay(resume_instance.id, job_description)
        
        return redirect('dashboard') # Redirect immediately
    return render(request, 'resumes/upload.html')