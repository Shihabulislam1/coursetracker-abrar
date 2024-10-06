from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from datetime import date
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Course, CourseCategory, CourseType, LessonLog
from .serializers import (
    CourseSerializer,
    CourseCategorySerializer,
    CourseTypeSerializer,
    LessonLogSerializer,
)
from .permissions import IsOwnerOrReadOnly, IsStaffOrReadOnly


class CourseTypeListCreateAPIView(ListCreateAPIView):
    queryset = CourseType.objects.all().order_by("name")
    serializer_class = CourseTypeSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]


class CourseTypeRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = CourseType.objects.all()
    serializer_class = CourseTypeSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]


class CourseCategoryListCreateAPIView(ListCreateAPIView):
    queryset = CourseCategory.objects.all().order_by("name")
    serializer_class = CourseCategorySerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]


class CourseCategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]


class CourseListCreateAPIView(ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        q = self.request.query_params.get("q", None)
        user = self.request.user

        # if query parameter is not provided, return all courses
        if not q:
            return Course.objects.filter(user=user)

        # if query parameter is provided, filter courses by name
        return Course.objects.filter(user=user, name__icontains=q)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="q",
                type=str,
                required=False,
                description="Search courses by name",
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CourseRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class LessonLogListCreateAPIView(ListCreateAPIView):
    serializer_class = LessonLogSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Check whether already log exists for the current course today
        user = self.request.user
        course = serializer.validated_data["course"]

        # Get the date of today and check whether log exists for the current course.
        today = date.today()

        # Check whether log exists for the current course today
        if LessonLog.objects.filter(user=user, course=course, date=today).exists():
            # Edit the existing log
            log = LessonLog.objects.get(user=user, course=course, date=today)
            log.duration = serializer.validated_data["duration"]

            # Save the log
            log.save()
        else:
            serializer.save(user=self.request.user, date=today)

    def get_queryset(self):
        user = self.request.user
        # Filter by date_from and date_to
        date_from = self.request.query_params.get("date_from", None)
        date_to = self.request.query_params.get("date_to", None)

        if date_from and date_to and date_from <= date_to:
            return LessonLog.objects.filter(user=user, date__range=[date_from, date_to])

        return LessonLog.objects.filter(user=user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="date_from",
                type=str,
                required=False,
                description="Filter logs from this date",
            ),
            OpenApiParameter(
                name="date_to",
                type=str,
                required=False,
                description="Filter logs to this date",
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class LessonLogRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = LessonLog.objects.all()
    serializer_class = LessonLogSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
