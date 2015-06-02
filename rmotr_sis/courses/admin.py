from django.contrib import admin

from .models import Lecture, Course, CourseInstance


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_instance', 'published')
    list_filter = ('published',)
    search_fields = ('title',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseInstance)
class CourseInstanceAdmin(admin.ModelAdmin):
    pass
