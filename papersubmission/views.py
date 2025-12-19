from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TheoryPaper
from .forms import PaperUploadForm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from student.models import Student
from teacher.models import Teacher

@login_required
def upload_paper(request):
    if not hasattr(request.user, 'student'):
        messages.error(request, 'Access denied. Only students can upload papers.')
        return redirect('student_dashboard')  # Adjust to existing dashboard URL
    student = request.user.student
    if not student.status:
        messages.error(request, 'Your account is not approved yet. Please wait for admin approval.')
        return redirect('student_dashboard')
    if request.method == 'POST':
        form = PaperUploadForm(request.POST, request.FILES)
        if form.is_valid():
            paper = form.save(commit=False)
            paper.student = student
            paper.save()
            messages.success(request, 'Paper uploaded successfully.')
            return redirect('student_dashboard')
    else:
        form = PaperUploadForm()
    return render(request, 'papersubmission/upload.html', {'form': form})

@login_required
def search_paper(request):
    if not hasattr(request.user, 'student'):
        messages.error(request, 'Access denied.')
        return redirect('student_dashboard')
    student = request.user.student
    if not student.status:
        messages.error(request, 'Your account is not approved yet. Please wait for admin approval.')
        return redirect('student_dashboard')
    paper = None
    if request.method == 'POST':
        enrollment = request.POST.get('enrollment')
        if enrollment == student.enrollment_number:
            paper = TheoryPaper.objects.filter(student=student, status='checked').first()
            if paper:
                return generate_pdf(request, paper.pk)
            else:
                messages.error(request, 'No checked paper found.')
        else:
            messages.error(request, 'Invalid enrollment number.')
    return render(request, 'papersubmission/search.html', {'student': student, 'paper': paper})

@login_required
def list_pending_papers(request):
    if not (request.user.is_staff or hasattr(request.user, 'teacher')):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')  # Adjust
    papers = TheoryPaper.objects.filter(status='pending').order_by('-submission_date')
    return render(request, 'papersubmission/pending_list.html', {'papers': papers})

@login_required
def review_paper(request, pk):
    if not (request.user.is_staff or hasattr(request.user, 'teacher')):
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    paper = get_object_or_404(TheoryPaper, pk=pk, status='pending')
    if request.method == 'POST':
        paper.marks = request.POST.get('marks')
        paper.feedback = request.POST.get('feedback')
        paper.status = 'checked'
        if hasattr(request.user, 'teacher'):
            paper.checked_by = request.user.teacher
        paper.save()
        messages.success(request, 'Paper reviewed successfully.')
        return redirect('papersubmission:list_pending_papers')
    return render(request, 'papersubmission/review.html', {'paper': paper})

@login_required
def student_papers(request):
    if not hasattr(request.user, 'student'):
        messages.error(request, 'Access denied.')
        return redirect('student_dashboard')
    student = request.user.student
    if not student.status:
        messages.error(request, 'Your account is not approved yet. Please wait for admin approval.')
        return redirect('student_dashboard')
    papers = TheoryPaper.objects.filter(student=student).order_by('-submission_date')
    return render(request, 'papersubmission/student_papers.html', {'papers': papers})

@login_required
def generate_pdf(request, pk):
    if not hasattr(request.user, 'student'):
        messages.error(request, 'Access denied.')
        return redirect('student_dashboard')
    student = request.user.student
    if not student.status:
        messages.error(request, 'Your account is not approved yet. Please wait for admin approval.')
        return redirect('student_dashboard')
    paper = get_object_or_404(TheoryPaper, pk=pk, status='checked', student=student)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="checked_paper_{paper.student.enrollment_number}.pdf"'
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 50
    p.drawString(50, y, f"Checked Theory Paper")
    y -= 20
    p.drawString(50, y, f"Student: {paper.student.get_name}")
    y -= 20
    p.drawString(50, y, f"Enrollment Number: {paper.student.enrollment_number}")
    y -= 20
    p.drawString(50, y, f"Course: {paper.course.course_name}")
    y -= 20
    p.drawString(50, y, f"Marks Obtained: {paper.marks}/10")
    y -= 20
    p.drawString(50, y, f"Feedback: {paper.feedback}")
    y -= 20
    p.drawString(50, y, f"Checked By: {paper.checked_by.get_name if paper.checked_by else 'Admin'}")
    y -= 20
    p.drawString(50, y, f"Submission Date: {paper.submission_date.strftime('%Y-%m-%d %H:%M')}")
    # Note: Original paper file can be downloaded separately via media URL
    p.save()
    buffer.seek(0)
    response.write(buffer.read())
    return response
