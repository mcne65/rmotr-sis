from django.contrib import admin

from applications.models import ApplicationReferral, Application


def mark_unselected(modeladmin, request, queryset):
    queryset.update(selected=False)

mark_unselected.short_description = "Un-Select applications (selected=False)"


def mark_selected(modeladmin, request, queryset):
    queryset.update(selected=True)

mark_selected.short_description = "Select applications (selected=True)"


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

    actions = [mark_selected, mark_unselected]
