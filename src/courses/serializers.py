from rest_framework import serializers
from .models import CourseType, CourseCategory, Course, LessonLog


class CourseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseType
        fields = "__all__"


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonLog
        fields = "__all__"

        # Make date readonly
        read_only_fields = ["date"]
