# resumes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # The home page is now the upload form
    path('', views.screen_resumes, name='upload_resumes'),
    
    # The new dashboard page
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # The action for the shortlist button
    path('shortlist/<int:result_id>/', views.shortlist_candidate, name='shortlist_candidate'),
    
    # The action for the export button
    path('export/excel/', views.export_excel, name='export_excel'),
]