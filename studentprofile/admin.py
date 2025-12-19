from django.contrib import admin
from .models import StudentProfileRequest, Paper, PaperRequest, Feedback

@admin.register(StudentProfileRequest)
class StudentProfileRequestAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'roll_no', 'status', 'submitted_at']
    list_filter = ['status', 'course']
    search_fields = ['student__user__username', 'roll_no']

@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'teacher', 'uploaded_at']
    list_filter = ['course', 'teacher']
    search_fields = ['title']

@admin.register(PaperRequest)
class PaperRequestAdmin(admin.ModelAdmin):
    list_display = ['student', 'paper', 'status', 'requested_at']
    list_filter = ['status']
    search_fields = ['student__user__username', 'paper__title']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['paper_request', 'submitted_at']
    search_fields = ['paper_request__student__user__username']
