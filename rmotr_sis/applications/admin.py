from django.contrib import admin

from applications.models import ApplicationReferral, Application


@admin.register(ApplicationReferral)
class ApplicationReferralAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    list_filter = ('active', )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):

    def skills_correct(self, obj):
        return obj.skills_assessment_correct_count
    skills_correct.short_description = 'Skills'

    list_display = ('id',
                    'batch',
                    'first_name',
                    'last_name',
                    'email',
                    'email_validated',
                    'status',
                    'need_scholarship',
                    'skills_correct',
                    'selected',
                    'charge_id',
                    'modified')
    list_filter = ('batch',
                   'email_validated',
                   'status',
                   'gender',
                   'selected',
                   'need_scholarship')
    search_fields = ('id',
                     'email',
                     'first_name',
                     'last_name')
