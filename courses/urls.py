from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LectureViewSet, NoteViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lectures', LectureViewSet, basename='lecture')
router.register(r'notes', NoteViewSet, basename='note')

urlpatterns = [
    path('', include(router.urls)),
]
