from django.contrib import admin
from .models import Teacher
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def approve_teachers(modeladmin, request, queryset):
    updated = queryset.update(status=True)
    if updated:
        messages.success(request, f'{updated} teacher(s) approved successfully.')
        # Send approval emails
        for teacher in queryset:
            subject = 'Account Approved - LJ University'
            message = f'Dear {teacher.user.first_name},\n\nYour teacher account has been approved. You can now log in and access the system.\n\nBest regards,\nLJ University Administration'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [teacher.user.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

approve_teachers.short_description = "Approve selected teachers"

def reject_teachers(modeladmin, request, queryset):
    rejected_count = 0
    for teacher in queryset:
        user = teacher.user
        # Send rejection email
        subject = 'Account Rejected - LJ University'
        message = f'Dear {user.first_name},\n\nWe regret to inform you that your teacher account application has been rejected. Please contact administration for more details.\n\nBest regards,\nLJ University Administration'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        user.delete()
        teacher.delete()
        rejected_count += 1
    if rejected_count:
        messages.success(request, f'{rejected_count} teacher(s) rejected and removed.')

reject_teachers.short_description = "Reject selected teachers"

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'mobile', 'address', 'status', 'salary']
    list_filter = ['status', 'address']
    search_fields = ['user__first_name', 'user__last_name', 'mobile']
    list_editable = ['status', 'salary']
    actions = [approve_teachers, reject_teachers]

    def get_name(self, obj):
        return obj.get_name
    get_name.short_description = 'Name'
