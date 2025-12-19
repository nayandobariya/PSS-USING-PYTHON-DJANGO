from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from datetime import date, timedelta
from exam import models as QMODEL
from student import models as SMODEL
from exam import forms as QFORM
from django.core.mail import send_mail


# for showing signup/login button for teacher
def teacherclick_view(request):
    if request.user.is_authenticated:
        # Fix redirect to correct URL path with leading slash
        return HttpResponseRedirect('/teacher/teacher_dashboard/')
    return render(request, 'teacher/teacherclick.html')


def teacher_signup_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/teacher/teacher_dashboard/')
    userForm = forms.TeacherUserForm()
    teacherForm = forms.TeacherForm()
    mydict = {'userForm': userForm, 'teacherForm': teacherForm}
    if request.method == 'POST':
        userForm = forms.TeacherUserForm(request.POST)
        teacherForm = forms.TeacherForm(request.POST, request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            teacher = teacherForm.save(commit=False)
            teacher.user = user
            teacher.status = False  # Require approval for new registrations
            teacher.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
            # Send registration confirmation email
            subject = 'Registration Successful - LJ University'
            message = f'Dear {user.first_name},\n\nYour teacher account has been created successfully. Your application is pending approval. You will receive an email once your account is approved.\n\nBest regards,\nLJ University Administration'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            # Redirect to waiting for approval page instead of auto-login
            return render(request, 'teacher/teacher_wait_for_approval.html')
    return render(request, 'teacher/teachersignup.html', context=mydict)


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_teacher_approved(user):
    """Check if teacher is approved (has status=True)"""
    if is_teacher(user):
        try:
            teacher = models.Teacher.objects.get(user=user)
            return teacher.status
        except models.Teacher.DoesNotExist:
            return False
    return False


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    from papersubmission.models import TheoryPaper
    teacher = models.Teacher.objects.get(user=request.user)  # ✅ get logged in teacher
    context = {
        'total_course': QMODEL.Course.objects.all().count(),
        'total_question': QMODEL.Question.objects.all().count(),
        'total_student': SMODEL.Student.objects.all().count(),
        'pending_papers': TheoryPaper.objects.filter(status='pending').count(),
        'pending_student': SMODEL.Student.objects.all().filter(status=False).count(),
        'teacher': teacher,   # ✅ pass teacher
    }
    return render(request, 'teacher/teacher_dashboard.html', context=context)


@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher_approved)
def teacher_exam_view(request):
    return render(request, 'teacher/teacher_exam.html')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_exam_view(request):
    courseForm = QFORM.CourseForm()
    if request.method == 'POST':
        courseForm = QFORM.CourseForm(request.POST)
        if courseForm.is_valid():
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-exam')
    return render(request, 'teacher/teacher_add_exam.html', {'courseForm': courseForm})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher_approved)
def teacher_view_exam_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'teacher/teacher_view_exam.html', {'courses': courses})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher_approved)
def delete_exam_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/teacher/teacher-view-exam')

@login_required(login_url='adminlogin')
def teacher_question_view(request):
    return render(request, 'teacher/teacher_question.html')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_question_view(request):
    questionForm = QFORM.QuestionForm()
    if request.method == 'POST':
        questionForm = QFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            question = questionForm.save(commit=False)
            course = QMODEL.Course.objects.get(id=request.POST.get('courseID'))
            question.course = course
            question.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/teacher/teacher-view-question')
    return render(request, 'teacher/teacher_add_question.html', {'questionForm': questionForm})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher_approved)
def teacher_view_question_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'teacher/teacher_view_question.html', {'courses': courses})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher_approved)
def see_question_view(request, pk):
    questions = QMODEL.Question.objects.all().filter(course_id=pk)
    return render(request, 'teacher/see_question.html', {'questions': questions})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher_approved)
def remove_question_view(request, pk):
    question = QMODEL.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/teacher/teacher-view-question')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher_approved)
def teacher_profile_view(request):
    teacher = models.Teacher.objects.get(user=request.user)
    return render(request, 'teacher/teacher_profile.html', {'teacher': teacher})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher_approved)
def teacher_view_pending_student_view(request):
    if request.method == 'POST':
        selected = request.POST.getlist('selected')
        action = request.POST.get('action')
        if action == 'approve_selected':
            for student_id in selected:
                student = SMODEL.Student.objects.get(id=student_id)
                student.status = True
                student.save()
        elif action == 'reject_selected':
            for student_id in selected:
                student = SMODEL.Student.objects.get(id=student_id)
                user = User.objects.get(id=student.user_id)
                user.delete()
                student.delete()
        return HttpResponseRedirect('/teacher/teacher-view-pending-student')
    students= SMODEL.Student.objects.all().filter(status=False)
    return render(request,'teacher/teacher_view_pending_student.html',{'students':students})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher_approved)
def teacher_approve_student_view(request, pk):
    student = SMODEL.Student.objects.get(id=pk)
    student.status = True
    student.save()
    return HttpResponseRedirect('/teacher/teacher-view-pending-student')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher_approved)
def teacher_reject_student_view(request, pk):
    student = SMODEL.Student.objects.get(id=pk)
    user = User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/teacher/teacher-view-pending-student')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher_approved)
def teacher_approve_all_students_view(request):
    students = SMODEL.Student.objects.all().filter(status=False)
    for student in students:
        student.status = True
        student.save()
    return HttpResponseRedirect('/teacher/teacher-view-pending-student')
