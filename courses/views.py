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
from core.services import get_youtube_service
import logging

logger = logging.getLogger(__name__)


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
        Note: This endpoint is deprecated. Use lecture-specific video URLs instead.
        """
        course = self.get_object()
        return Response({
            'error': 'Please use the lecture-specific video URL endpoint.',
            'course_id': course.id,
            'message': 'Use GET /api/lectures/{lecture_id}/get_video_url/ instead'
        }, status=status.HTTP_400_BAD_REQUEST)


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
        Get YouTube embed URL for lecture video.
        
        This endpoint generates a secure YouTube embed URL for the video.
        Access is controlled through enrollment checks - only enrolled students
        and course instructors can access this endpoint.
        
        Videos should be uploaded as "Unlisted" on YouTube for privacy.
        The backend controls who can access the embed URL.
        """
        lecture = self.get_object()
        
        if not lecture.youtube_video_id:
            return Response({
                'error': 'YouTube video ID not found for this lecture.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        try:
            youtube_service = get_youtube_service()
            
            # Get query parameters for embed options
            autoplay = request.query_params.get('autoplay', 'false').lower() == 'true'
            controls = request.query_params.get('controls', 'true').lower() != 'false'
            
            # Generate embed URL
            embed_url = youtube_service.get_embed_url(
                video_id=lecture.youtube_video_id,
                autoplay=autoplay,
                controls=controls
            )
            
            # Also get watch URL for reference
            watch_url = youtube_service.get_watch_url(lecture.youtube_video_id)
            
            return Response({
                'lecture_id': lecture.id,
                'lecture_title': lecture.title,
                'youtube_video_id': lecture.youtube_video_id,
                'embed_url': embed_url,
                'watch_url': watch_url,
                'message': 'Use embed_url in an iframe to display the video. Access is controlled by enrollment.'
            })
        
        except ValueError as e:
            logger.error(f"Invalid YouTube video ID: {str(e)}")
            return Response({
                'error': f'Invalid YouTube video ID: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.error(f"Error generating video URL: {str(e)}")
            return Response({
                'error': 'Failed to generate video URL. Please try again later.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
        Get file URL for note (PDF, etc.).
        
        This endpoint returns the direct URL to the note file.
        Access is controlled through enrollment checks - only enrolled students
        and course instructors can access this endpoint.
        
        Files can be hosted on Google Drive, Dropbox, or any public URL.
        For Google Drive, use the sharing link format.
        """
        note = self.get_object()
        
        if not note.file_url:
            return Response({
                'error': 'File URL not found for this note.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'note_id': note.id,
            'note_title': note.title,
            'file_type': note.file_type,
            'file_url': note.file_url,
            'message': 'Access is controlled by enrollment. Use this URL to access the file.'
        })
