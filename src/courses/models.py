from django.db import models
from django.contrib.auth import get_user_model
import uuid


# Create your models here.
class CourseType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class CourseCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    required_unit = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Foreign Key. Null if deleted
    course_type = models.ForeignKey(CourseType, on_delete=models.SET_NULL, null=True)
    course_category = models.ForeignKey(
        CourseCategory, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.name


class LessonLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    duration = models.PositiveIntegerField()
    date = models.DateField()

    # Foreign Key. Null if deleted
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.course.name} - {self.date}"
