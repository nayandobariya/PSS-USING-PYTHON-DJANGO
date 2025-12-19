from django.contrib import admin
from .models import Course, Question, Result

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_name', 'question_number', 'total_marks']
    list_filter = ['course_name']
    search_fields = ['course_name']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['course', 'question', 'marks', 'answer']
    list_filter = ['course']
    search_fields = ['question', 'course__course_name']

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'marks', 'date']
    list_filter = ['exam', 'date']
    search_fields = ['student__user__first_name', 'student__user__last_name', 'exam__course_name']
