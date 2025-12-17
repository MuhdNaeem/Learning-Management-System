from rest_framework import permissions
from enrollments.models import Enrollment


class IsInstructorOrAdmin(permissions.BasePermission):
    """
    Permission to only allow instructors or admins to access.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            (request.user.is_instructor or request.user.is_admin)
        )


class IsEnrolledOrInstructor(permissions.BasePermission):
    """
    Permission to only allow enrolled students or instructors to access course content.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Instructors and admins can access everything
        if request.user.is_instructor or request.user.is_admin:
            return True
        
        # For students, check enrollment
        course_id = view.kwargs.get('course_id') or view.kwargs.get('pk')
        if course_id:
            return Enrollment.objects.filter(
                user=request.user,
                course_id=course_id,
                is_active=True
            ).exists()
        
        # If no course_id, allow (will be checked in has_object_permission)
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_instructor or request.user.is_admin:
            return True
        
        # For students, check if they're enrolled in the course
        course = getattr(obj, 'course', None)
        if course is None:
            # If object is a course itself
            course = obj if hasattr(obj, 'instructor') else None
        
        if course:
            return Enrollment.objects.filter(
                user=request.user,
                course=course,
                is_active=True
            ).exists()
        
        return False


class IsCourseInstructor(permissions.BasePermission):
    """
    Permission to only allow the course instructor to modify the course.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        return obj.instructor == request.user


class IsLectureOwner(permissions.BasePermission):
    """
    Permission to only allow the course instructor to modify lectures.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        return obj.course.instructor == request.user
