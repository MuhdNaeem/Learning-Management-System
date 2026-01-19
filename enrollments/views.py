from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Enrollment
from .serializers import EnrollmentSerializer, EnrollmentCreateSerializer
from permissions.permissions import IsInstructorOrAdmin


class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Enrollment management.
    """
    queryset = Enrollment.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return EnrollmentCreateSerializer
        return EnrollmentSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_instructor or user.is_admin:
            # Instructors and admins can see all enrollments
            return Enrollment.objects.all()
        else:
            # Students see only their own enrollments
            return Enrollment.objects.filter(user=user, is_active=True)
    
    def get_permissions(self):
        # Only instructors and admins can create enrollments
        if self.action == 'create':
            return [IsInstructorOrAdmin()]
        elif self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsInstructorOrAdmin()]
    
    def create(self, request, *args, **kwargs):
        """
        Create an enrollment.
        Only instructors and admins can create enrollments.
        They can enroll any user by providing user_id, or themselves if omitted.
        """
        serializer = EnrollmentCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        enrollment = serializer.save()
        
        return Response(
            EnrollmentSerializer(enrollment).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unenroll(self, request, pk=None):
        """Unenroll from a course"""
        enrollment = self.get_object()
        
        # Only the enrolled user or admin can unenroll
        if enrollment.user != request.user and not request.user.is_admin:
            return Response(
                {'error': 'You do not have permission to unenroll this user.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        enrollment.is_active = False
        enrollment.save()
        
        return Response(
            {'message': 'Successfully unenrolled from the course.'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_enrollments(self, request):
        """Get current user's enrollments"""
        enrollments = Enrollment.objects.filter(
            user=request.user,
            is_active=True
        )
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)
