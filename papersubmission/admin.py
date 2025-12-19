from django.contrib import admin
from .models import TheoryPaper

@admin.register(TheoryPaper)
class TheoryPaperAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'marks', 'submission_date')
    list_filter = ('status', 'course')
    search_fields = ('student__user__username', 'course__course_name')
