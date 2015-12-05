from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from accounts.models import User


class AccountsUserAdmin(UserAdmin):

    list_display = ('username',
                    'email',
                    'first_name',
                    'last_name',
                    'timezone',
                    'last_activity',
                    'is_active',
                    'is_staff')
    fieldsets = (
        (_('Credentials'), {'fields': ('username',
                                       'password')}),
        (_('Personal info'), {'fields': ('first_name',
                                         'last_name',
                                         'email',
                                         'gender',
                                         'birth_date',
                                         'timezone')}),
        (_('Extra information'), {'fields': ('occupation',
                                             'objective',
                                             'application')}),
        (_('External accounts'), {'fields': ('twitter_handle',
                                             'github_handle',
                                             'cloud9_handle',
                                             'linkedin_profile_url')}),
        (_('Permissions'), {'fields': ('is_active',
                                       'is_staff',
                                       'is_superuser',
                                       'groups',
                                       'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',
                                           'date_joined',
                                           'last_activity')}),
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups',
                   'courseinstance___code')

admin.site.register(User, AccountsUserAdmin)
