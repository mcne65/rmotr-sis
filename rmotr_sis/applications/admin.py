from django.contrib import admin

from applications.models import ApplicationReferral, Application


@admin.register(ApplicationReferral)
class ApplicationReferralAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    list_filter = ('active', )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    pass
