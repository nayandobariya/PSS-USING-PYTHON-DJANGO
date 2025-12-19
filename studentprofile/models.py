from django.db import models
from student.models import Student
from teacher.models import Teacher
from exam.models import Course

class StudentProfileRequest(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, default='')
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, default='')
    roll_no = models.CharField(max_length=20)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending'
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.get_name} - {self.course.course_name if self.course else 'No Course'}"

class Paper(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    excel_file = models.FileField(upload_to='excels/', null=True, blank=True)
    paper_file = models.FileField(upload_to='papers/', null=True, blank=True)
    title = models.CharField(max_length=200)
    selected_students = models.ManyToManyField(Student, related_name='selected_papers', blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        student_name = self.student.get_name if self.student else "General"
        return f"{self.title} - {student_name} - {self.course.course_name}"

class PaperRequest(models.Model):
    id = models.BigAutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[('requested', 'Requested'), ('approved', 'Approved'), ('denied', 'Denied')],
        default='requested'
    )
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.get_name} - {self.paper.title}"

class StudentPaper(models.Model):
    id = models.BigAutoField(primary_key=True)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    paper_file = models.FileField(upload_to='papers/', null=True, blank=True)

    def __str__(self):
        return f"{self.paper.title} - {self.student.get_name}"

class Feedback(models.Model):
    id = models.BigAutoField(primary_key=True)
    paper_request = models.ForeignKey(PaperRequest, on_delete=models.CASCADE)
    feedback_text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.paper_request} by {self.paper_request.student.get_name}"
