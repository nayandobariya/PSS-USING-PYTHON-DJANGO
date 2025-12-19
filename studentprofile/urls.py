from django.urls import path
from . import views

app_name = 'studentprofile'

urlpatterns = [
    path('profile/', views.student_profile_view, name='student_profile'),
    path('request-form/', views.request_form_view, name='request_form'),
    path('raise-request/<int:paper_id>/', views.raise_request_view, name='raise_request'),
    path('give-feedback/<int:request_id>/', views.give_feedback_view, name='give_feedback'),
    path('teacher/upload/', views.teacher_upload_view, name='teacher_upload'),
    path('teacher/dashboard/', views.teacher_dashboard_view, name='teacher_dashboard'),
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin/approve-request/<int:request_id>/', views.approve_request_view, name='approve_request'),
    path('admin/approve-paper-request/<int:pr_id>/', views.approve_paper_request_view, name='approve_paper_request'),
]
