from django.db import models
from django.conf import settings


class Course(models.Model):
    """
    Course model representing a course in the LMS.
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses_taught',
        limit_choices_to={'role': 'instructor'}
    )
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'courses'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Lecture(models.Model):
    """
    Lecture model representing a single lecture/video in a course.
    """
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lectures'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    youtube_video_id = models.CharField(
        max_length=100,
        help_text='YouTube video ID (e.g., "dQw4w9WgXcQ" from https://www.youtube.com/watch?v=dQw4w9WgXcQ)'
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text='Order of lecture in the course'
    )
    duration_minutes = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Duration of the video in minutes'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'lectures'
        ordering = ['course', 'order', 'created_at']
        unique_together = ['course', 'order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Note(models.Model):
    """
    Note model representing PDFs or other materials for a lecture.
    """
    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
        related_name='notes'
    )
    title = models.CharField(max_length=200)
    file_url = models.URLField(
        max_length=500,
        help_text='Direct URL to the note file (can be Google Drive, Dropbox, or any public URL)'
    )
    file_type = models.CharField(
        max_length=50,
        default='pdf',
        help_text='File type (pdf, docx, etc.)'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notes'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.lecture.title} - {self.title}"
