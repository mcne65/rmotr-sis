from django.contrib import admin

from .models import Lecture, Batch, Course, CourseInstance


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_instance', 'published')
    list_filter = ('published',)
    search_fields = ('title',)
    raw_id_fields = ('assignments',)


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('number', 'start_date', 'accepting_applications')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseInstance)
class CourseInstanceAdmin(admin.ModelAdmin):
    list_display = ('code', 'course', 'professor', 'start_date', 'end_date')
