from django.contrib import admin
from .models import Enrollment


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'is_active', 'enrolled_at', 'completed_at']
    list_filter = ['is_active', 'enrolled_at']
    search_fields = ['user__username', 'course__title']
    readonly_fields = ['enrolled_at']
