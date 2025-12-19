from django.db import models
from django.core.validators import MinValueValidator
from student.models import Student
from teacher.models import Teacher
from exam.models import Course

class TheoryPaper(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    paper_file = models.FileField(upload_to='theory_papers/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('checked', 'Checked')], default='pending')
    marks = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    feedback = models.TextField(null=True, blank=True)
    checked_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.get_name} - {self.course.course_name}"
