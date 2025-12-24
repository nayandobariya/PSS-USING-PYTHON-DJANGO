wo# Fix Student Exam Website Issues

## Issues Identified
- Bootstrap version mismatch: Templates use 3.0.0, global.css uses 4.5.2
- Potential character encoding problems
- CSS styling inconsistencies in MCQ display

## Tasks
- [ ] Update Bootstrap links from 3.0.0 to 4.5.2 in all affected templates
- [ ] Ensure UTF-8 character encoding in all templates
- [ ] Verify CSS compatibility and styling consistency
- [ ] Test MCQ display and character rendering

## Files to Update
- [x] templates/student/take_exam.html
- [x] templates/student/start_exam.html
- [x] templates/student/student_exam.html
- [x] templates/student/check_marks.html
- [x] templates/student/student_marks.html
- [ ] templates/student/view_result.html
- [ ] templates/teacher/teacher_view_exam.html
- [ ] templates/teacher/see_question.html
- [ ] templates/teacher/teacher_view_question.html
- [ ] templates/exam/admin_check_marks.html
- [ ] templates/exam/admin_view_course.html
- [ ] templates/exam/admin_view_marks.html
- [ ] templates/exam/admin_view_teacher.html
- [ ] templates/exam/admin_view_student_marks.html
- [ ] templates/exam/admin_view_teacher_salary.html
- [ ] templates/exam/admin_view_question.html
- [ ] templates/exam/admin_view_pending_teacher.html
- [ ] templates/exam/view_question.html
