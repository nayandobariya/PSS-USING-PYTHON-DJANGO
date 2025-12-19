from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_paper, name='upload_paper'),
    path('search/', views.search_paper, name='search_paper'),
    path('pending/', views.list_pending_papers, name='list_pending_papers'),
    path('review/<int:pk>/', views.review_paper, name='review_paper'),
    path('pdf/<int:pk>/', views.generate_pdf, name='generate_pdf'),
    path('papers/', views.student_papers, name='student_papers'),
]
