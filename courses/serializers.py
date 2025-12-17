from rest_framework import serializers
from .models import Course, Lecture, Note


class NoteSerializer(serializers.ModelSerializer):
    """Serializer for Note model"""
    
    class Meta:
        model = Note
        fields = ['id', 'title', 'file_key', 'file_type', 'created_at']
        read_only_fields = ['id', 'created_at']


class LectureSerializer(serializers.ModelSerializer):
    """Serializer for Lecture model"""
    notes = NoteSerializer(many=True, read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    
    class Meta:
        model = Lecture
        fields = [
            'id', 'course', 'course_title', 'title', 'description',
            'video_key', 'order', 'duration_minutes', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for Course model"""
    instructor_name = serializers.CharField(source='instructor.get_full_name', read_only=True)
    lecture_count = serializers.IntegerField(source='lectures.count', read_only=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'instructor', 'instructor_name',
            'is_published', 'lecture_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CourseDetailSerializer(CourseSerializer):
    """Detailed serializer for Course with lectures"""
    lectures = LectureSerializer(many=True, read_only=True)
    
    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ['lectures']
