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
    """Serializer for creating enrollment"""
    
    class Meta:
        model = Enrollment
        fields = ['course']
    
    def create(self, validated_data):
        user = self.context['request'].user
        enrollment, created = Enrollment.objects.get_or_create(
            user=user,
            course=validated_data['course'],
            defaults={'is_active': True}
        )
        if not created and not enrollment.is_active:
            enrollment.is_active = True
            enrollment.save()
        return enrollment
