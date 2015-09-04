from django.contrib import admin

from scholarships.models import ScholarshipApplication


@admin.register(ScholarshipApplication)
class ScholarshipApplicationAdmin(admin.ModelAdmin):
    pass
