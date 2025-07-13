# resumes/models.py
from django.db import models

class Resume(models.Model):
    """
    This model now just keeps a record of the original uploaded file.
    """
    resume_file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.resume_file.name

class ScreeningResult(models.Model):
    """
    This new model stores all the processed data for our dashboard.
    """
    filename = models.CharField(max_length=255)
    score = models.FloatField()
    skills = models.JSONField(default=list)  # Stores the list of skills found
    missing_skills = models.JSONField(default=list) # Stores the list of missing skills
    is_shortlisted = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.filename} - Score: {self.score}"

    class Meta:
        ordering = ['-score'] # Default ordering by score descending