from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lecture, Note
from .serializers import (
    CourseSerializer,
    CourseDetailSerializer,
    LectureSerializer,
    NoteSerializer
)
from permissions.permissions import (
    IsInstructorOrAdmin,
    IsEnrolledOrInstructor,
    IsCourseInstructor,
    IsLectureOwner
)


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Course management.
    """
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsInstructorOrAdmin(), IsCourseInstructor()]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_instructor or user.is_admin:
            # Instructors see all courses
            return Course.objects.all()
        else:
            # Students see only published courses they're enrolled in
            from enrollments.models import Enrollment
            enrolled_courses = Enrollment.objects.filter(
                user=user,
                is_active=True
            ).values_list('course_id', flat=True)
            return Course.objects.filter(
                id__in=enrolled_courses,
                is_published=True
            )
    
    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)
    
    @action(detail=True, methods=['get'], permission_classes=[IsEnrolledOrInstructor])
    def lectures(self, request, pk=None):
        """Get all lectures for a course"""
        course = self.get_object()
        lectures = course.lectures.all()
        serializer = LectureSerializer(lectures, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], permission_classes=[IsEnrolledOrInstructor])
    def get_video_url(self, request, pk=None):
        """
        Get signed URL for course video.
        This is a placeholder - actual implementation will generate signed URLs
        from S3/CloudFront.
        """
        course = self.get_object()
        # TODO: Implement signed URL generation
        return Response({
            'message': 'Video URL generation will be implemented with S3/CloudFront',
            'course_id': course.id
        })


class LectureViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Lecture management.
    """
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsEnrolledOrInstructor()]
        return [IsInstructorOrAdmin(), IsLectureOwner()]
    
    def get_queryset(self):
        user = self.request.user
        course_id = self.request.query_params.get('course_id')
        
        if user.is_instructor or user.is_admin:
            if course_id:
                return Lecture.objects.filter(course_id=course_id)
            return Lecture.objects.all()
        else:
            # Students see only lectures from enrolled courses
            from enrollments.models import Enrollment
            enrolled_courses = Enrollment.objects.filter(
                user=user,
                is_active=True
            ).values_list('course_id', flat=True)
            queryset = Lecture.objects.filter(course_id__in=enrolled_courses)
            if course_id:
                queryset = queryset.filter(course_id=course_id)
            return queryset
    
    @action(detail=True, methods=['get'], permission_classes=[IsEnrolledOrInstructor])
    def get_video_url(self, request, pk=None):
        """
        Get signed URL for lecture video.
        This is a placeholder - actual implementation will generate signed URLs
        from S3/CloudFront.
        """
        lecture = self.get_object()
        # TODO: Implement signed URL generation
        return Response({
            'message': 'Video URL generation will be implemented with S3/CloudFront',
            'lecture_id': lecture.id,
            'video_key': lecture.video_key
        })
    
    @action(detail=True, methods=['get'], permission_classes=[IsEnrolledOrInstructor])
    def notes(self, request, pk=None):
        """Get all notes for a lecture"""
        lecture = self.get_object()
        notes = lecture.notes.all()
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)


class NoteViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Note management.
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsEnrolledOrInstructor()]
        return [IsInstructorOrAdmin()]
    
    def get_queryset(self):
        user = self.request.user
        lecture_id = self.request.query_params.get('lecture_id')
        
        if user.is_instructor or user.is_admin:
            if lecture_id:
                return Note.objects.filter(lecture_id=lecture_id)
            return Note.objects.all()
        else:
            # Students see only notes from enrolled courses
            from enrollments.models import Enrollment
            enrolled_courses = Enrollment.objects.filter(
                user=user,
                is_active=True
            ).values_list('course_id', flat=True)
            queryset = Note.objects.filter(
                lecture__course_id__in=enrolled_courses
            )
            if lecture_id:
                queryset = queryset.filter(lecture_id=lecture_id)
            return queryset
    
    @action(detail=True, methods=['get'], permission_classes=[IsEnrolledOrInstructor])
    def get_file_url(self, request, pk=None):
        """
        Get signed URL for note file.
        This is a placeholder - actual implementation will generate signed URLs
        from S3/CloudFront.
        """
        note = self.get_object()
        # TODO: Implement signed URL generation
        return Response({
            'message': 'File URL generation will be implemented with S3/CloudFront',
            'note_id': note.id,
            'file_key': note.file_key
        })
