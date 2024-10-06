from django.contrib import admin

from .models import Course, CourseCategory, CourseType, LessonLog

admin.site.register(Course)
admin.site.register(CourseCategory)
admin.site.register(CourseType)
admin.site.register(LessonLog)

# Register your models here.
