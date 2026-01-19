from rest_framework import serializers
from .models import Enrollment
from courses.serializers import CourseSerializer


class EnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for Enrollment model"""
    course = CourseSerializer(read_only=True)
    course_id = serializers.IntegerField(write_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'user', 'user_name', 'course', 'course_id',
            'enrolled_at', 'is_active', 'completed_at'
        ]
        read_only_fields = ['id', 'user', 'enrolled_at']


class EnrollmentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating enrollment.
    Only instructors and admins can create enrollments.
    They can enroll any user (specified by user_id) or themselves.
    """
    user_id = serializers.IntegerField(required=False, write_only=True)
    course_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Enrollment
        fields = ['user_id', 'course_id']
    
    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        
        # Only instructors and admins can create enrollments
        if not (user.is_instructor or user.is_admin):
            raise serializers.ValidationError({
                'error': 'Only instructors and admins can create enrollments.'
            })
        
        # If user_id is not provided, use the requesting user
        if 'user_id' not in attrs or attrs['user_id'] is None:
            attrs['user_id'] = user.id
        
        return attrs
    
    def create(self, validated_data):
        from accounts.models import User
        from courses.models import Course
        
        user_id = validated_data.pop('user_id')
        course_id = validated_data.pop('course_id')
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                'user_id': 'User not found.'
            })
        
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise serializers.ValidationError({
                'course_id': 'Course not found.'
            })
        
        enrollment, created = Enrollment.objects.get_or_create(
            user=user,
            course=course,
            defaults={'is_active': True}
        )
        
        if not created and not enrollment.is_active:
            enrollment.is_active = True
            enrollment.save()
        
        return enrollment
