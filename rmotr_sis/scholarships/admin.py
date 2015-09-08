from django.contrib import admin

from scholarships.models import ScholarshipReferral, ScholarshipApplication


@admin.register(ScholarshipReferral)
class ScholarshipReferralAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    list_filter = ('active', )


@admin.register(ScholarshipApplication)
class ScholarshipApplicationAdmin(admin.ModelAdmin):
    pass
