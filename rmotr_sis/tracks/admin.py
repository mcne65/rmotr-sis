from django.contrib import admin
from suit.admin import SortableModelAdmin, SortableTabularInline
from tracks.models import Unit, Lesson, ReadingLesson, AssignmentLesson


class LessonInline(SortableTabularInline):
    model = Lesson
    sortable = 'order'


@admin.register(Unit)
class UnitAdmin(SortableModelAdmin):
    sortable = 'order'
    inlines = (LessonInline,)
    search_fields = ('name', )


@admin.register(Lesson)
class LessonAdmin(SortableModelAdmin):
    def full_name(self, lesson):
        return '{} - {}'.format(lesson.order, lesson.name)
    list_display = ('full_name', 'unit', 'order')
    sortable = 'order'
    list_filter = ('unit',)
    search_fields = ('name', )


@admin.register(ReadingLesson)
class ReadingLessonAdmin(admin.ModelAdmin):
    pass


@admin.register(AssignmentLesson)
class AssignmentLessonAdmin(admin.ModelAdmin):
    pass
