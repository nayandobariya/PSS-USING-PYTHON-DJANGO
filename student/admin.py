from django.contrib import admin
from .models import Student
from django.contrib import messages
from django.http import HttpResponseRedirect

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'mobile', 'address', 'status', 'approval_actions']
    list_filter = ['address', 'status']
    search_fields = ['user__first_name', 'user__last_name', 'mobile']
    actions = ['approve_students', 'reject_students']
    
    def get_name(self, obj):
        return obj.get_name
    get_name.short_description = 'Name'
    
    def approval_actions(self, obj):
        if obj.status:
            return "Approved"
        else:
            return "Pending Approval"
    approval_actions.short_description = 'Status'
    
    def approve_students(self, request, queryset):
        updated = queryset.update(status=True)
        self.message_user(request, f'{updated} student(s) were successfully approved.', messages.SUCCESS)
    approve_students.short_description = "Approve selected students"
    
    def reject_students(self, request, queryset):
        # Delete the students and their user accounts
        for student in queryset:
            user = student.user
            student.delete()
            user.delete()
        self.message_user(request, f'{queryset.count()} student(s) were rejected and deleted.', messages.SUCCESS)
    reject_students.short_description = "Reject and delete selected students"
