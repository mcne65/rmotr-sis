from django.contrib import admin

from .models import Lecture, Course, CourseInstance, Assignment, AssignmentAttempt

admin.site.register(Lecture)
admin.site.register(Course)
admin.site.register(CourseInstance)
admin.site.register(Assignment)
admin.site.register(AssignmentAttempt)
