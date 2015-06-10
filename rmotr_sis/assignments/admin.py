from django.contrib import admin

from .models import Assignment, AssignmentAttempt


@admin.register(AssignmentAttempt)
class AssignmentAttemptAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'start_datetime',
                    'end_datetime', 'resolved')
    list_filter = ('resolved',)
    search_fields = ('assignment__title', 'student__username')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'tag_list')
    list_filter = ('difficulty', )
    search_fields = ('id', 'title', 'tags__name')
