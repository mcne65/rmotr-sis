from django.contrib import admin

from applications.models import ApplicationReferral, Application


@admin.register(ApplicationReferral)
class ApplicationReferralAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    list_filter = ('active', )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'batch', 'first_name', 'last_name', 'email', 'modified',
                    'status', 'skills_assessment_correct_count')
    list_filter = ('batch', 'email_validated', 'status', 'gender')
