import csv
from datetime import datetime

from django.contrib import admin
from django.http import HttpResponse

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

    actions = ['mark_selected', 'mark_unselected', 'export_to_csv']

    def mark_unselected(self, request, queryset):
        rows_updated = queryset.update(selected=False)
        self.message_user(request, "{} application(s) updated".format(
            rows_updated))

    mark_unselected.short_description = ("Un-Select applications"
                                         " (selected=False)")

    def mark_selected(self, request, queryset):
        rows_updated = queryset.update(selected=True)
        self.message_user(request, "{} application(s) updated".format(
            rows_updated))

    mark_selected.short_description = "Select applications (selected=True)"

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        file_name = 'attachment; filename="applications-{}.csv"'.format(
            datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
        response['Content-Disposition'] = file_name

        writer = csv.writer(response)
        writer.writerow(['id', 'First Name', 'Last Name', 'email'])
        for app in queryset:
            writer.writerow([app.id, app.first_name, app.last_name, app.email])

        return response

    export_to_csv.short_description = "Export to CSV"
