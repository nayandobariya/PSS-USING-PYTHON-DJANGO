import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinexam.settings')
django.setup()

from django.contrib.auth.models import User
from student.models import Student
from django.contrib.auth import authenticate
from django.test import RequestFactory
from student.views import registration_view
from django.core.files.uploadedfile import SimpleUploadedFile

def test_registration_flow():
    print("Testing Student Registration Flow...")

    # Create a test request
    factory = RequestFactory()

    # Simulate POST data
    post_data = {
        'register': 'register',
        'userForm-first_name': 'Test',
        'userForm-last_name': 'Student',
        'userForm-username': 'teststudent123',
        'userForm-password': 'testpass123',
        'userForm-email': 'test@example.com',
        'studentForm-mobile': '1234567890',
        'studentForm-address': 'Test Address',
        'studentForm-profile_pic': SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
    }

    # Create request
    request = factory.post('/student/registration/', data=post_data, files={'studentForm-profile_pic': SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")})

    # Call the view
    try:
        response = registration_view(request)
        print("Registration view called successfully")
        print(f"Response status: {response.status_code}")

        # Check if student was created
        try:
            user = User.objects.get(username='teststudent123')
            student = Student.objects.get(user=user)
            print(f"Student created: {student.user.username}, status: {student.status}")
        except User.DoesNotExist:
            print("User was not created")
        except Student.DoesNotExist:
            print("Student was not created")

    except Exception as e:
        print(f"Error during registration: {e}")

    # Check database state
    print(f"Total students: {Student.objects.count()}")
    print(f"Students with status=False: {Student.objects.filter(status=False).count()}")
    print(f"Students with status=True: {Student.objects.filter(status=True).count()}")

    # Check if status is True
    if student.status:
        print("Student status is True - can login")
    else:
        print("Student status is False - cannot login")

    # Cleanup
    try:
        user = User.objects.get(username='teststudent123')
        user.delete()
        print("Test user cleaned up")
    except:
        pass

if __name__ == '__main__':
    test_registration_flow()
