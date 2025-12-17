from django.contrib import admin
from .models import Course, Lecture, Note


class LectureInline(admin.TabularInline):
    model = Lecture
    extra = 1
    ordering = ['order']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'is_published', 'created_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'description']
    inlines = [LectureInline]


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'duration_minutes', 'created_at']
    list_filter = ['course', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['course', 'order']


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'lecture', 'file_type', 'created_at']
    list_filter = ['file_type', 'created_at']
    search_fields = ['title']
