from django.contrib import admin

from .models import Lecture, Course, CourseInstance, Assignment, AssignmentAttempt


class AssignmentAttemptAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'start_datetime',
                    'end_datetime', 'resolved')


admin.site.register(Lecture)
admin.site.register(Course)
admin.site.register(CourseInstance)
admin.site.register(Assignment)
admin.site.register(AssignmentAttempt, AssignmentAttemptAdmin)
