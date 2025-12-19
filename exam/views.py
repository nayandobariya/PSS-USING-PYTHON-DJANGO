from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from teacher import models as TMODEL
from student import models as SMODEL
from teacher import forms as TFORM
from student import forms as SFORM
from student.views import generate_enrollment_number
from django.contrib.auth.models import User
from django.contrib import messages



def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'exam/index.html')


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def afterlogin_view(request):
    if is_student(request.user):
        # Check if student is approved
        try:
            student = SMODEL.Student.objects.get(user=request.user)
            if student.status:
                return redirect('student_dashboard')
            else:
                return render(request,'student/student_wait_for_approval.html')
        except SMODEL.Student.DoesNotExist:
            return redirect('studentlogin')

    elif is_teacher(request.user):
        accountapproval=TMODEL.Teacher.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('teacher-dashboard')
        else:
            return render(request,'teacher/teacher_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')



def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    from papersubmission.models import TheoryPaper
    from studentprofile.models import PaperRequest
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    'total_course':models.Course.objects.all().count(),
    'total_question':models.Question.objects.all().count(),
    'pending_papers':TheoryPaper.objects.filter(status='pending').count(),
    'pending_student':SMODEL.Student.objects.all().filter(status=False).count(),
    'approved_student':SMODEL.Student.objects.all().filter(status=True).count(),
    'pending_teacher':TMODEL.Teacher.objects.all().filter(status=False).count(),
    'total_paper_requests':PaperRequest.objects.all().count(),
    'approved_paper_requests':PaperRequest.objects.filter(status='approved').count(),
    'pending_paper_requests':PaperRequest.objects.filter(status='pending').count(),
    }
    return render(request,'exam/admin_dashboard.html',context=dict)

@login_required(login_url='adminlogin')
def admin_teacher_view(request):
    dict={
    'total_teacher':TMODEL.Teacher.objects.all().filter(status=True).count(),
    'pending_teacher':TMODEL.Teacher.objects.all().filter(status=False).count(),
    'salary':TMODEL.Teacher.objects.all().filter(status=True).aggregate(Sum('salary'))['salary__sum'],
    }
    return render(request,'exam/admin_teacher.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_teacher_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=True)
    return render(request,'exam/admin_view_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
def update_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=TMODEL.User.objects.get(id=teacher.user_id)
    userForm=TFORM.TeacherUserForm(instance=user)
    teacherForm=TFORM.TeacherForm(request.FILES,instance=teacher)
    mydict={'userForm':userForm,'teacherForm':teacherForm}
    if request.method=='POST':
        userForm=TFORM.TeacherUserForm(request.POST,instance=user)
        teacherForm=TFORM.TeacherForm(request.POST,request.FILES,instance=teacher)
        if userForm.is_valid() and teacherForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            teacherForm.save()
            return redirect('admin-view-teacher')
    return render(request,'exam/update_teacher.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-teacher')




@login_required(login_url='adminlogin')
def admin_view_pending_teacher_view(request):
    if request.method == 'POST':
        selected = request.POST.getlist('selected')
        action = request.POST.get('action')
        if action == 'approve_selected':
            for teacher_id in selected:
                teacher = TMODEL.Teacher.objects.get(id=teacher_id)
                teacher.status = True
                teacher.save()
        elif action == 'reject_selected':
            for teacher_id in selected:
                teacher = TMODEL.Teacher.objects.get(id=teacher_id)
                user = User.objects.get(id=teacher.user_id)
                user.delete()
                teacher.delete()
        return HttpResponseRedirect('/admin-view-pending-teacher')
    teachers= TMODEL.Teacher.objects.all().filter(status=False)
    return render(request,'exam/admin_view_pending_teacher.html',{'teachers':teachers})


@login_required(login_url='adminlogin')
def approve_teacher_view(request,pk):
    teacherSalary=forms.TeacherSalaryForm()
    if request.method=='POST':
        teacherSalary=forms.TeacherSalaryForm(request.POST)
        if teacherSalary.is_valid():
            teacher=TMODEL.Teacher.objects.get(id=pk)
            teacher.salary=teacherSalary.cleaned_data['salary']
            teacher.status=True
            teacher.save()

        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-pending-teacher')
    return render(request,'exam/salary_form.html',{'teacherSalary':teacherSalary})

@login_required(login_url='adminlogin')
def reject_teacher_view(request,pk):
    teacher=TMODEL.Teacher.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    # Send rejection email before deleting
    subject = 'Account Rejected - LJ University'
    message = f'Dear {user.first_name},\n\nWe regret to inform you that your teacher account application has been rejected. Please contact administration for more details.\n\nBest regards,\nLJ University Administration'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    user.delete()
    teacher.delete()
    return HttpResponseRedirect('/admin-view-pending-teacher')

@login_required(login_url='adminlogin')
def admin_view_teacher_salary_view(request):
    teachers= TMODEL.Teacher.objects.all().filter(status=True)
    return render(request,'exam/admin_view_teacher_salary.html',{'teachers':teachers})




@login_required(login_url='adminlogin')
def admin_student_view(request):
    dict={
    'total_student':SMODEL.Student.objects.all().count(),
    'pending_student':SMODEL.Student.objects.all().filter(status=False).count(),
    'approved_student':SMODEL.Student.objects.all().filter(status=True).count(),
    }
    return render(request,'exam/admin_student.html',context=dict)

@login_required(login_url='adminlogin')
def admin_view_pending_student_view(request):
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
        return HttpResponseRedirect('/admin-view-pending-student')
    students= SMODEL.Student.objects.all().filter(status=False)
    return render(request,'exam/admin_view_pending_student.html',{'students':students})

@login_required(login_url='adminlogin')
def approve_all_students_view(request):
    students = SMODEL.Student.objects.all().filter(status=False)
    for student in students:
        student.status = True
        student.save()
    return HttpResponseRedirect('/admin-view-pending-student')

@login_required(login_url='adminlogin')
def approve_all_teachers_view(request):
    teachers = TMODEL.Teacher.objects.all().filter(status=False)
    for teacher in teachers:
        teacher.status = True
        teacher.save()
    return HttpResponseRedirect('/admin-view-pending-teacher')

@login_required(login_url='adminlogin')
def approve_student_view(request, pk):
    student = SMODEL.Student.objects.get(id=pk)
    student.status = True
    student.save()

    # Send approval email to student
    subject = 'Account Approved - LJ University'
    message = f'Dear {student.user.first_name},\n\nYour student account has been approved by the administrator. You can now log in to your account.\n\nBest regards,\nLJ University Administration'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [student.user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    return HttpResponseRedirect('/admin-view-pending-student')

@login_required(login_url='adminlogin')
def reject_student_view(request, pk):
    student = SMODEL.Student.objects.get(id=pk)
    user = User.objects.get(id=student.user_id)

    user.delete()
    student.delete()
    return HttpResponseRedirect('/admin-view-pending-student')

@login_required(login_url='adminlogin')
def admin_add_student_view(request):
    userForm=SFORM.StudentUserForm()
    studentForm=SFORM.StudentForm()
    csvForm=forms.StudentCSVUploadForm()
    mydict={'userForm':userForm,'studentForm':studentForm,'csvForm':csvForm}
    if request.method=='POST':
        if 'manual_submit' in request.POST:
            userForm=SFORM.StudentUserForm(request.POST)
            studentForm=SFORM.StudentForm(request.POST,request.FILES)
            if userForm.is_valid() and studentForm.is_valid():
                user=userForm.save()
                user.set_password(user.password)
                user.save()
                student=studentForm.save(commit=False)
                student.user=user
                student.status=True  # Admin-added students are approved immediately
                student.enrollment_number = generate_enrollment_number()  # Generate unique enrollment number
                student.save()
                my_student_group = Group.objects.get_or_create(name='STUDENT')
                my_student_group[0].user_set.add(user)

                # Send email notification to the new student if email is provided
                if user.email:
                    subject = 'Account Created - LJ University'
                    message = f'Dear {user.first_name},\n\nYour student account has been created by the administrator. You can now log in to your account.\n\nUsername: {user.username}\n\nBest regards,\nLJ University Administration'
                    from_email = settings.EMAIL_HOST_USER
                    recipient_list = [user.email]
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                return HttpResponseRedirect('/admin-view-student')
            else:
                print("form is invalid")
        elif 'csv_submit' in request.POST:
            csvForm=forms.StudentCSVUploadForm(request.POST, request.FILES)
            if csvForm.is_valid():
                csv_file = request.FILES['csv_file']
                import csv
                import io

                # Read the raw file content
                raw_content = csv_file.read()

                # Decode with utf-8 fallback without chardet
                try:
                    decoded_file = raw_content.decode('utf-8')
                except UnicodeDecodeError:
                    try:
                        decoded_file = raw_content.decode('windows-1252')
                    except UnicodeDecodeError:
                        try:
                            decoded_file = raw_content.decode('iso-8859-1')
                        except UnicodeDecodeError:
                            messages.error(request, 'Unable to decode the CSV file. Please ensure it is saved as UTF-8 or a compatible encoding.')
                            return HttpResponseRedirect('/admin-add-student')

                # Use newline='' when opening the CSV string buffer to fix new-line character error
                io_string = io.StringIO(decoded_file, newline='')
                reader = csv.DictReader(io_string, skipinitialspace=True)
                success_count = 0
                errors = []
                row_count = 0

                # Debug: Print column names
                print(f"CSV columns: {reader.fieldnames}")

                for row in reader:
                    row_count += 1
                    
                    # Skip empty rows
                    if not any(row.values()):
                        print(f"Skipping empty row {row_count}")
                        continue
                    
                    print(f"Processing row {row_count}: {row}")
                    try:
                        # Strip keys and values in row dict to avoid mismatch due to unwanted spaces
                        row = {k.strip() if k else '': (v.strip() if v and isinstance(v, str) else (v if v else '')) for k, v in row.items()}
                        
                        # Validate required fields
                        required_fields = ['first_name', 'last_name', 'username', 'address', 'mobile']
                        
                        for field in required_fields:
                            value = row.get(field, '')
                            if not value or (isinstance(value, str) and not value.strip()):
                                raise ValueError(f"Missing or empty required field: {field}")

                        # Handle password - use default if empty
                        password = row.get('password', '').strip()
                        if not password:
                            password = 'default_password_123'

                        # Check if username already exists
                        username = row['username'].strip()
                        if User.objects.filter(username=username).exists():
                            raise ValueError(f"Username '{username}' already exists")

                        # Create user
                        user = User.objects.create_user(
                            username=username,
                            password=password,
                            first_name=row['first_name'].strip(),
                            last_name=row['last_name'].strip(),
                            email=row.get('email', '').strip() if row.get('email') else ''
                        )

                        # Create student
                        student = SMODEL.Student.objects.create(
                            user=user,
                            address=row['address'].strip(),
                            mobile=row['mobile'].strip(),
                            status=True,  # Auto-approved
                            enrollment_number=generate_enrollment_number()
                        )

                        # Add to STUDENT group
                        my_student_group = Group.objects.get_or_create(name='STUDENT')
                        my_student_group[0].user_set.add(user)

                        success_count += 1
                        print(f"Successfully created student: {user.username}")
                    except Exception as e:
                        error_msg = f"Row {row_count}: {str(e)}"
                        errors.append(error_msg)
                        print(f"Error in row {row_count}: {str(e)}")

                print(f"Total rows processed: {row_count}, Success: {success_count}, Errors: {len(errors)}")
                if success_count == 0:
                    messages.error(request, 'No students were added. Please check the CSV file content and format.')
                else:
                    messages.success(request, f'Successfully added {success_count} students.')

                if errors:
                    messages.warning(request, f'Errors encountered: {"; ".join(errors)}')
                return HttpResponseRedirect('/admin-view-student')
    return render(request,'exam/admin_add_student.html',context=mydict)

@login_required(login_url='adminlogin')
def admin_view_student_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'exam/admin_view_student.html',{'students':students})



@login_required(login_url='adminlogin')
def update_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=SMODEL.User.objects.get(id=student.user_id)
    userForm=SFORM.StudentUserForm(instance=user)
    studentForm=SFORM.StudentForm(request.FILES,instance=student)
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=SFORM.StudentUserForm(request.POST,instance=user)
        studentForm=SFORM.StudentForm(request.POST,request.FILES,instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            studentForm.save()
            return redirect('admin-view-student')
    return render(request,'exam/update_student.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_student_view(request,pk):
    student=SMODEL.Student.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return HttpResponseRedirect('/admin-view-student')


@login_required(login_url='adminlogin')
def admin_course_view(request):
    return render(request,'exam/admin_course.html')


@login_required(login_url='adminlogin')
def admin_add_course_view(request):
    courseForm=forms.CourseForm()
    if request.method=='POST':
        courseForm=forms.CourseForm(request.POST)
        if courseForm.is_valid():        
            courseForm.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-course')
    return render(request,'exam/admin_add_course.html',{'courseForm':courseForm})


@login_required(login_url='adminlogin')
def admin_view_course_view(request):
    courses = models.Course.objects.all()
    return render(request,'exam/admin_view_course.html',{'courses':courses})

@login_required(login_url='adminlogin')
def delete_course_view(request,pk):
    course=models.Course.objects.get(id=pk)
    course.delete()
    return HttpResponseRedirect('/admin-view-course')



@login_required(login_url='adminlogin')
def admin_question_view(request):
    return render(request,'exam/admin_question.html')


@login_required(login_url='adminlogin')
def admin_add_question_view(request):
    questionForm=forms.QuestionForm()
    if request.method=='POST':
        questionForm=forms.QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            course=models.Course.objects.get(id=request.POST.get('courseID'))
            question.course=course
            question.save()       
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-question')
    return render(request,'exam/admin_add_question.html',{'questionForm':questionForm})


@login_required(login_url='adminlogin')
def admin_view_question_view(request):
    courses= models.Course.objects.all()
    return render(request,'exam/admin_view_question.html',{'courses':courses})

@login_required(login_url='adminlogin')
def view_question_view(request,pk):
    questions=models.Question.objects.all().filter(course_id=pk)
    return render(request,'exam/view_question.html',{'questions':questions})

@login_required(login_url='adminlogin')
def delete_question_view(request,pk):
    question=models.Question.objects.get(id=pk)
    question.delete()
    return HttpResponseRedirect('/admin-view-question')

@login_required(login_url='adminlogin')
def admin_view_student_marks_view(request):
    students= SMODEL.Student.objects.all()
    return render(request,'exam/admin_view_student_marks.html',{'students':students})

@login_required(login_url='adminlogin')
def admin_view_marks_view(request,pk):
    courses = models.Course.objects.all()
    response =  render(request,'exam/admin_view_marks.html',{'courses':courses})
    response.set_cookie('student_id',str(pk))
    return response

@login_required(login_url='adminlogin')
def admin_check_marks_view(request,pk):
    course = models.Course.objects.get(id=pk)
    student_id = request.COOKIES.get('student_id')
    student= SMODEL.Student.objects.get(id=student_id)

    results= models.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'exam/admin_check_marks.html',{'results':results})
    




def aboutus_view(request):
    return render(request,'exam/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'exam/contactussuccess.html')
    return render(request, 'exam/contactus.html', {'form':sub})


def forgot_password_view(request):
    form = forms.ForgotPasswordForm()
    if request.method == 'POST':
        form = forms.ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            new_password = form.cleaned_data['new_password']

            # Try to find user by username or email
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                try:
                    user = User.objects.get(email=username)
                except User.DoesNotExist:
                    form.add_error('username', 'User with this username or email does not exist.')
                    return render(request, 'exam/forgot_password.html', {'form': form})

            # Update password
            user.set_password(new_password)
            user.save()

            return render(request, 'exam/password_reset_complete.html', {'message': 'Password has been reset successfully. You can now log in with your new password.'})

    return render(request, 'exam/forgot_password.html', {'form': form})




