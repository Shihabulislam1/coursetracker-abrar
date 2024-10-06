from django.urls import path, include

from .views import (
    CourseTypeListCreateAPIView,
    CourseTypeRetrieveUpdateDestroyAPIView,
    CourseCategoryListCreateAPIView,
    CourseCategoryRetrieveUpdateDestroyAPIView,
    CourseListCreateAPIView,
    CourseRetrieveUpdateDestroyAPIView,
    LessonLogListCreateAPIView,
    LessonLogRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("types/", CourseTypeListCreateAPIView.as_view(), name="course-types"),
    path(
        "types/<uuid:pk>/",
        CourseTypeRetrieveUpdateDestroyAPIView.as_view(),
        name="course-type",
    ),
    path(
        "categories/",
        CourseCategoryListCreateAPIView.as_view(),
        name="course-categories",
    ),
    path(
        "categories/<uuid:pk>/",
        CourseCategoryRetrieveUpdateDestroyAPIView.as_view(),
        name="course-category",
    ),
    path("", CourseListCreateAPIView.as_view(), name="courses"),
    path("<uuid:pk>/", CourseRetrieveUpdateDestroyAPIView.as_view(), name="course"),
    path("logs/", LessonLogListCreateAPIView.as_view(), name="lesson-logs"),
    path(
        "logs/<uuid:pk>/",
        LessonLogRetrieveUpdateDestroyAPIView.as_view(),
        name="lesson-log",
    ),
]
