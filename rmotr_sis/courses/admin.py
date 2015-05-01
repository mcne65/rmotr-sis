from django.contrib import admin

from .models import Lecture, Course, CourseInstance

admin.site.register(Lecture)
admin.site.register(Course)
admin.site.register(CourseInstance)
