from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('registration/', views.registration_view, name='registration'),
    path('signup/', views.student_signup_view, name='student_signup'),
    path('dashboard/', views.student_dashboard_view, name='student_dashboard'),
    path('studentclick/', views.studentclick_view, name='studentclick'),
    path('studentlogin/', views.student_login_view, name='studentlogin'),
    path('exam/', views.student_exam_view, name='student_exam'),
    path('take-exam/<int:pk>/', views.take_exam_view, name='take_exam'),
    path('start-exam/<int:pk>/', views.start_exam_view, name='start_exam'),
    path('calculate-marks/', views.calculate_marks_view, name='calculate_marks'),
    path('view-result/', views.view_result_view, name='view_result'),
    path('check-marks/<int:pk>/', views.check_marks_view, name='check_marks'),
    path('marks/', views.student_marks_view, name='student_marks'),
    path('profile/', views.student_profile_view, name='student_profile'),
]
