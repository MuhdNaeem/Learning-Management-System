from django.db import models
from django.conf import settings


class Enrollment(models.Model):
    """
    Enrollment model representing the relationship between a user and a course.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'enrollments'
        unique_together = ['user', 'course']
        ordering = ['-enrolled_at']
    
    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"
