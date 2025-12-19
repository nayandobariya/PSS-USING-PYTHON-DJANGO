import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinexam.settings')
django.setup()

from django.contrib.auth.models import User
from student.models import Student
from django.contrib.auth import authenticate

def test_student_approval():
    print("Testing Student Approval System...")

    # Test 1: Create a new student (status should be False)
    user = User.objects.create_user(username='teststudent', password='testpass', first_name='Test', last_name='Student', email='test@example.com')
    student = Student.objects.create(user=user, mobile='1234567890', address='Test Address', status=False)
    print(f"Created student: {student.user.username}, status: {student.status}")

    # Test 2: Try to authenticate (should work)
    auth_user = authenticate(username='teststudent', password='testpass')
    if auth_user:
        print("Authentication successful")
    else:
        print("Authentication failed")

    # Test 3: Check if student is approved (should be False)
    if student.status:
        print("Student is approved")
    else:
        print("Student is NOT approved - should show waiting page")

    # Test 4: Simulate approval
    student.status = True
    student.save()
    print(f"After approval: status = {student.status}")

    # Cleanup
    student.delete()
    user.delete()
    print("Test completed and cleaned up")

if __name__ == '__main__':
    test_student_approval()
